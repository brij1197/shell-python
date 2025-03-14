import sys


def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")

    # Wait for user input
    command=input()
    
    if command.startswith('exit'):
        parts = command.split()
        if len(parts) > 1:
            try:
                exit_code = int(parts[1])
                sys.exit(exit_code)
            except ValueError:
                print(f'exit: {parts[1]}: numeric argument required')
        else:
            sys.exit(0)
      
    print(f'{command}: command not found')
    
    main()


if __name__ == "__main__":
    main()
