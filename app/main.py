import sys
import shutil

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
            print(f'{parts[1]} is a shell builtin\n')
        elif path :=shutil.which(parts[1]):
            print(f'{parts[1]} is {path}\n')
        else:
            print(f'{parts[1]}: not found')
    else:
        print('type: missing argument')

def main():
  
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
            print(f'{command}: command not found')
        
    main()


if __name__ == "__main__":
    main()
