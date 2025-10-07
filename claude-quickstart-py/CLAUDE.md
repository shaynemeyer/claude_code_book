# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python 3.11 quickstart project demonstrating basic Python project structure with a greeting function. The project uses only Python standard library modules and follows a clean src/tests organization.

## Development Commands

### Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Running the Application
```bash
python src/app.py Alice
# or without arguments (defaults to "Developer")
python src/app.py
```

### Running the HTTP Server
```bash
python src/server.py
# Then test with: curl 'http://localhost:8000/hello?name=Alice'
```

### Running Tests
```bash
python -m unittest
# or run individual test files
python -m unittest tests.test_app
```

## Architecture

The project follows a simple structure:

- **src/app.py**: Contains the main `greet()` function that validates input and returns JSON-serializable greeting messages
- **src/server.py**: HTTP server using standard library that exposes `/hello?name=X` endpoint, integrates with greet() function
- **tests/test_app.py**: Unit tests for the greet() function using Python's built-in unittest framework
- **tests/test_server.py**: Integration tests for the HTTP server, including ephemeral port testing and clean shutdown

The application provides both a CLI interface (src/app.py) and HTTP API (src/server.py).

## Key Technical Details

- Python version: 3.11 (specified in .python-version)
- No external dependencies - uses only standard library
- Type hints used throughout for better code clarity
- Input validation with proper error handling (ValueError for invalid inputs)
- JSON output format for structured data exchange