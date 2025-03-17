from abc import ABC, abstractmethod
import os
import sys
import shutil
import subprocess
import shlex
import io
from typing import List, Optional

class Command(ABC):
    @abstractmethod
    def execute(self,args:List[str])->None:
        pass
    
    @property
    @abstractmethod
    def name(self)->str:
        pass
    
class Exit(Command):
    @property
    def name(self)->str:
        return "exit"
    
    def execute(self,args:List[str])->None:
        if len(args)>1:
            try:
                exit_code = int(args[1])
                sys.exit(exit_code)
            except ValueError:
                print(f'exit: {args[1]}: numeric argument required')
        else:
            sys.exit(0)

class Echo(Command):
    @property
    def name(self) -> str:
        return "echo"
    
    def execute(self, args: List[str]) -> None:
        if len(args) == 1:
            print()
            return
        
        result = []
        for arg in args[1:]:
            if arg.startswith("'") and arg.endswith("'"):
                result.append(arg[1:-1])
            else:
                result.append(arg)
        
        print(" ".join(result))
            
class Pwd(Command):
    @property
    def name(self)->str:
        return "pwd"
    
    def execute(self,args:List[str])->None:
        print(os.getcwd())
        
class Type(Command):
    @property
    def name(self)->str:
        return "type"
    
    def execute(self,args:List[str])->None:
        if len(args)>1:
            self._check_command_type(args[1])
        else:
            print('type: missing argument')
    
    def _check_command_type(self,command:str)->None:
        if command in Shell.get_builtin_commands():
            print(f'{command} is a shell builtin')
        elif path := shutil.which(command):
            print(f'{command} is {path}')
        else:
            print(f'{command}: not found')
            
class Cd(Command):
    @property
    def name(self)->str:
        return "cd"
    
    def execute(self,args:List[str])->None:
        if len(args)==1:
            os.chdir(os.path.expanduser('~'))
            return
        
        if args[1]=='-':
            self._handle_previous_directory()
            return
        self._change_directory(args[1])
    
    def _handle_previous_directory(self)->None:
        old_pwd=os.getenv('OLDPWD')
        if old_pwd:
            current_pwd=os.getcwd()
            os.chdir(old_pwd)
            os.environ['OLDPWD']=current_pwd
        else:
            print('cd: OLDPWD not set')
    
    def _change_directory(self,path:str)->None:
        current=os.getcwd()
        try:
            os.chdir(os.path.expanduser(path))
            os.environ['OLDPWD']=current
        except FileNotFoundError:
            print(f'cd: {path}: No such file or directory')
        except NotADirectoryError:
            print(f'cd: {path}: Not a directory')
        except PermissionError:
            print(f'cd: {path}: Permission denied')
        
class ExternalCommand(Command):
    def __init__(self, command: str, original_name:str):
        self._command = command
        self._original_name=original_name
        
    @property
    def name(self) -> str:
        return self._original_name
    
    def execute(self, args: List[str]) -> None:
        try:
            pid = os.fork()
            if pid == 0:  # Child process
                # If stdout is redirected, set up the redirection
                if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.name != '<stdout>':
                    # Duplicate the file descriptor
                    fd = os.open(sys.stdout.name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
                    os.dup2(fd, 1)  # Redirect stdout to our file
                    os.close(fd)     # Close the original fd
                
                # Execute command with original name as argv[0]
                exec_args = [self._original_name] + args[1:]
                try:
                    os.execv(self._command, exec_args)
                except OSError as e:
                    print(f'Error executing {self._original_name}: {str(e)}', file=sys.stderr)
                    sys.exit(1)
            else:  # Parent process
                _, status = os.waitpid(pid, 0)
                if status != 0:
                    # Don't exit on error, just continue
                    pass
                
        except OSError as e:
            print(f'Error executing {self._original_name}: {str(e)}', file=sys.stderr)
            sys.stderr.flush()

class Shell:
    def __init__(self):
        self._commands={
            cmd.name: cmd for cmd in [
                Exit(),
                Echo(),
                Pwd(),
                Cd(),
                Type()
            ] 
        }
    
    @staticmethod
    def get_builtin_commands()->List[str]:
        return ['exit','echo','pwd','type','cd']
    
    def _split_command(self, input_line: str) -> tuple[list[str], str, str]:
        res = [""]
        current_quote = ""
        i = 0
        output_file = None
        
        while i < len(input_line):
            c = input_line[i]
            
            if c == "\\":
                if i + 1 >= len(input_line):
                    break
                ch = input_line[i + 1]
                if current_quote == "'":
                    res[-1] += c
                elif current_quote == '"':
                    if ch in ["\\", "$", '"', "\n"]:
                        res[-1] += ch
                    else:
                        res[-1] += "\\" + ch
                    i += 1
                else:
                    res[-1] += input_line[i + 1]
                    i += 1
            elif c in ['"', "'"]:
                if current_quote == "":
                    current_quote = c
                elif current_quote == c:
                    current_quote = ""
                else:
                    res[-1] += c
            elif c == " " and current_quote == "":
                if res[-1] != "":
                    res.append("")
            else:
                res[-1] += c
            i += 1
        
        if res[-1] == "":
            res.pop()
        
        if "1>" in res:
            idx = res.index("1>")
            command_parts, output_file = res[:idx], res[idx + 1]
        elif ">" in res:
            idx = res.index(">")
            command_parts, output_file = res[:idx], res[idx + 1]
        else:
            command_parts = res
            
        return command_parts, output_file
    
    def _get_command(self,cmd_name:str)->Optional[Command]:
        if cmd_name in self._commands:
            return self._commands[cmd_name]
        
        if os.path.isfile(cmd_name) and os.access(cmd_name, os.X_OK):
            return ExternalCommand(cmd_name,os.path.basename(cmd_name))
        
        for path in os.environ.get("PATH", "").split(os.pathsep):
            cmd_path = os.path.join(path, cmd_name)
            if os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
                return ExternalCommand(cmd_path,cmd_name)
        
        return None
    
    def run_command(self, input_line: str) -> None:
        try:
            args, output_file = self._split_command(input_line)
            if not args:
                return
                
            cmd_name = args[0]
            command_obj = self._get_command(cmd_name)
            
            if command_obj:
                original_stdout = sys.stdout
                try:
                    if output_file:
                        sys.stdout = open(output_file, 'w')
                    command_obj.execute(args)
                finally:
                    if output_file:
                        sys.stdout.close()
                    sys.stdout = original_stdout
            else:
                print(f"{cmd_name}: command not found")
                
        except ValueError as e:
            print(f"Error: {str(e)}")
        except IOError as e:
            print(f"Error: {str(e)}")
            
    
    def run(self)->None:
        while True:
            try:
                sys.stdout.write("$ ")
                command=input().strip()
                self.run_command(command)
            except EOFError:
                sys.exit(0)
            except KeyboardInterrupt:
                print()

def main():
    shell=Shell()
    shell.run()
    
if __name__=='__main__':
    main()