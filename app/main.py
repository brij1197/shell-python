import sys


def main():

    commands= ['exit','echo','type']
    
    sys.stdout.write("$ ")

    command=input().strip()
    
    match command:
        case command if command.startswith('exit'):
            parts = command.split()
            if len(parts) > 1:
                try:
                    exit_code = int(parts[1])
                    sys.exit(exit_code)
                except ValueError:
                    print(f'exit: {parts[1]}: numeric argument required')
            else:
                sys.exit(0)
        
        case command if command.startswith('echo'):
            print(command[5:])
        
        case command if command.startswith('type'):
            parts = command.split()
            if len(parts) > 1:
                if parts[1] in commands:
                    print(f'{parts[1]} is a shell builtin')
            else:
                print('type: missing argument')
        
        case _:
            print(f'{command}: command not found')
        
    main()


if __name__ == "__main__":
    main()
