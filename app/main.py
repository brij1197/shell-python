from abc import ABC, abstractmethod
import os
import sys
import shutil
import subprocess
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
    def name(self)->str:
        return "echo"
    
    def execute(self,args:List[str])->None:
        if len(args)==1:
            print()
            return
        
        message = " ".join(args[1:])

        # Remove any surrounding single quotes from the entire message
        if message.startswith("'") and message.endswith("'"):
            message = message[1:-1]
            
        print(message)
        
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
    def __init__(self,command:str):
        self._command=command
        
    @property
    def name(self)->str:
        return self._command
    
    def execute(self,args:List[str]):
        try:
            result=subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.rstrip(), file=sys.stderr)
            if result.returncode!=0:
                sys.exit(result.returncode)
                
        except subprocess.SubprocessError as e:
            print(f'Error executing {args[0]}:str{e}',file=sys.stderr)
            sys.exit(1)

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
    
    def _parse_command(self,input_line:str)->tuple[str,List[str]]:
        parts=input_line.strip().split()
        return parts[0] if parts else "",parts
    
    def _get_command(self,cmd_name:str)->Optional[Command]:
        if cmd_name in self._commands:
            return self._commands[cmd_name]
        
        if path:=shutil.which(cmd_name):
            return ExternalCommand(path)
        
        return None
    
    def run_command(self, input_line: str) -> None:
        cmd_name,args=self._parse_command(input_line)
        if not cmd_name:
            return
        
        command=self._get_command(cmd_name)
        if command:
            command.execute(args)
        else:
            print(f'{cmd_name}: command not found')
    
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