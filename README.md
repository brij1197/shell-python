# Python Shell Implementation

## Description
A custom shell implementation in Python that provides basic shell functionality, including built-in commands and external command execution. This shell supports command-line completion, I/O redirection, and basic file operations.

## Features
- **Built-in Commands:**
  - `exit` - Exit the shell with an optional exit code
  - `echo` - Display messages to standard output
  - `pwd` - Print working directory
  - `cd` - Change directory with support for `~` and `-` (previous directory)
  - `type` - Display command type (builtin or external)
- Command-line completion using the **Tab** key
- Support for external command execution
- I/O redirection (`>`, `>>`, `2>`, `2>>`)
- Quote handling for both single and double quotes
- Error handling for various file operations

## Prerequisites
- Python **3.x**
- Standard Python libraries (no additional dependencies required)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/python-shell.git
   ```
2. Navigate to the project directory:
   ```bash
   cd python-shell
   ```
3. Run the shell:
   ```bash
   ./yourprogram.sh
   ```

## Usage Examples
### Basic Command Usage
```bash
$ pwd
/current/working/directory

$ echo Hello World
Hello World

$ cd ~
$ cd -  # Return to the previous directory
```

### I/O Redirection
```bash
$ echo "Hello" > output.txt
$ echo "World" >> output.txt
```

### Command Type Checking
```bash
$ type echo
echo is a shell builtin

$ type python
python is /usr/bin/python
```

## Implementation Details
- **Object-oriented design** with the Command pattern
- **Abstract base class** for command implementation
- Support for both **built-in and external commands**
- **Robust command parsing** with quote handling
- **Command completion** using the `readline` module
- **File descriptor handling** for I/O redirection

## Error Handling
The shell includes comprehensive error handling for:
- File not found
- Permission denied
- Invalid directory operations
- Command execution errors
- Invalid command syntax
