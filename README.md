# Python Shell Implementation

## Description
A custom shell implementation in Python that provides basic shell functionality including built-in commands and external command execution. This shell supports command-line completion, I/O redirection, and basic file operations.

## Features
- Built-in Commands:
  - `exit` - Exit the shell with optional exit code
  - `echo` - Display messages to standard output
  - `pwd` - Print working directory
  - `cd` - Change directory with support for `~` and `-` (previous directory)
  - `type` - Display command type (builtin or external)
- Command-line completion using Tab key
- Support for external command execution
- I/O redirection (`>`, `>>`, `2>`, `2>>`)
- Quote handling for both single and double quotes
- Error handling for various file operations

## Prerequisites
- Python 3.x
- Standard Python libraries (no additional dependencies required)

## Installation
1. Clone the repository
2. Navigate to the project directory
3. Run the shell:
```bash
./yourprogram.sh
```

## Usage Examples
# Basic command usage
$ pwd
/current/working/directory

$ echo Hello World
Hello World

$ cd ~
$ cd -  # Return to previous directory

# I/O redirection
$ echo "Hello" > output.txt
$ echo "World" >> output.txt

# Command type checking
$ type echo
echo is a shell builtin
$ type python
python is /usr/bin/python

## Implementation Details
- Object-oriented design with Command pattern
- Abstract base class for command implementation
- Support for both built-in and external commands
- Robust command parsing with quote handling
- Command completion using readline module
- File descriptor handling for I/O redirection

## Error Handling
The shell includes comprehensive error handling for:
- File not found
- Permission denied
- Invalid directory operations
- Command execution errors
- Invalid command syntax

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
