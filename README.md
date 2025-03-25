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
- **Support for External Commands:**
  - Executes commands found in the system `$PATH`
  - Runs executable files directly if found
- **Command-line Completion:**
  - Uses the `readline` module to enable Tab completion for both built-in and external commands
  - Displays possible matches if multiple commands exist
- **I/O Redirection:**
  - Standard Output (`>`, `>>`)
  - Standard Error (`2>`, `2>>`)
  - Separate handling of `stdout` and `stderr` redirection
- **Quote Handling:**
  - Supports both single (`'`) and double (`"`) quotes
- **Error Handling:**
  - Handles file not found, permission denied, invalid directory operations, and command execution errors

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
   ./your_program.sh
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
$ echo "Error message" 2> error.log
$ echo "Append error" 2>> error.log
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
- **Support for both built-in and external commands**
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
- Missing arguments in built-in commands