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
