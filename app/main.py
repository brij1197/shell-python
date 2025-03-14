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
        
    elif command.startswith('echo'):
        print(command[5:])
        
    elif command.startswith('type'):
        parts = command.split()
        if len(parts) > 1:
            file_name = parts[1]
            try:
                with open(file_name, 'r') as file:
                    content = file.read()
                    print(content)
            except FileNotFoundError:
                print(f'type: {file_name}: No such file or directory')
        else:
            print('type: missing operand')
        
    else:
        print(f'{command}: command not found')
        
    main()


if __name__ == "__main__":
    main()
