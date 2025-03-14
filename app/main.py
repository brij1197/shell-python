import sys
import shutil
import subprocess

SHELL_COMMANDS= ['exit','echo','type']

def shell_exit(*args):
    parts=args[0]
    if len(parts)>1:
        try:
            exit_code = int(parts[1])
            sys.exit(exit_code)
        except ValueError:
            print(f'exit: {parts[1]}: numeric argument required')
    else:
        sys.exit(0)
        

def shell_echo(*args):
    print(args[0][5:])


def shell_type(*args):
    parts=args[0]
    if len(parts) > 1:
        if parts[1] in SHELL_COMMANDS:
            print(f'{parts[1]} is a shell builtin')
        elif path :=shutil.which(parts[1]):
            print(f'{parts[1]} is {path}')
        else:
            print(f'{parts[1]}: not found')
    else:
        print('type: missing argument')
        
def execute_external_command(command):
    parts=command.split()
    path=shutil.which(parts[0])
    
    if path:
        try:
            result=subprocess.run(
                parts,
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
            print(f'Error executing {parts[0]}:str{e}',file=sys.stderr)
            return False
        return True
    return False

def main():
    try:
        sys.stdout.write("$ ")

        command=input().strip()
        
        match command:
            case command if command.startswith('exit'):
                parts = command.split()
                shell_exit(parts)
            
            case command if command.startswith('echo'):
                shell_echo(command)
            
            case command if command.startswith('type'):
                parts = command.split()
                shell_type(parts)
            
            case _:
                if not execute_external_command(command):
                    print(f'{command}: command not found')
    except EOFError:
        sys.exit(0)
    except KeyboardInterrupt:
        print()
            

if __name__ == "__main__":
    while True:
        main()
