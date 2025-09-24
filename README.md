# litex-gsm8k-killer

An automated solution system for GSM8K mathematical problems using Litex and DeepSeek-R1 LLM for Litex code generation and verification.

## Overview

This project solves GSM8K (Grade School Math 8K) problems by:
1. Fetching tasks and examples from the Litex platform via API
2. Generating Litex code solutions using DeepSeek-R1 LLM with example-based learning
3. Verifying generated Litex code with Pylitex computational engine
4. Returning verified solutions for further processing

The system uses example-based learning to improve solution quality and employs Pylitex for robust Litex code verification. It automatically transforms fractions to decimal numbers when possible for better computational accuracy.

## Project Structure

```
litex-gsm8k-killer/
├── killer.py              # Main solution generation and verification logic
├── utils/
│   ├── __init__.py        # Empty package initializer
│   ├── http_utils.py      # HTTP utilities for Litex API communication
│   └── config_utils.py    # Configuration management utilities
├── test/
│   ├── __init__.py        # Empty package initializer
│   ├── basic_test.py      # Basic functionality test (single task)
│   └── batch_test.py      # Batch processing test with multiprocessing
├── config.json.temp       # Configuration template file
├── config.json           # Actual configuration (ignored by git)
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore patterns
└── README.md            # This file
```

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/litexlang/litex-gsm8k-killer.git
   cd litex-gsm8k-killer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials:**
   ```bash
   cp config.json.temp config.json
   # Edit config.json with your actual API keys and credentials
   ```

4. **Run a basic test:**
   ```bash
   python test/basic_test.py
   ```

## Setup

### 1. Prerequisites

- Python 3.8+
- Internet connection for API access
- Required Python packages (install via requirements.txt):
  ```bash
  pip install -r requirements.txt
  ```
  
  Dependencies include:
  ```bash
  pip install requests volcengine-python-sdk[ark] pylitex
  ```

### System Requirements
- **Memory**: Minimum 512MB RAM (recommended 1GB+)
- **Network**: Stable internet connection for API calls
- **Storage**: ~50MB for dependencies and project files
- **OS**: Linux, macOS, or Windows with Python support

### 2. Configuration

1. Copy the configuration template:
   ```bash
   cp config.json.temp config.json
   ```

2. Edit `config.json` with your actual credentials:
   ```json
   {
     "user_info": {
       "username": "your_username",
       "email": "your_email@example.com"
     },
     "collaboration_info": {
       "id": "your_collaboration_id"
     },
     "volcengine_info": {
       "api_key": "your_volcengine_api_key"
     }
   }
   ```

### 3. API Keys Setup

- **VolcEngine API Key**: Required for DeepSeek-R1 model access
- **Litex Platform Access**: Ensure you have valid collaboration_info credentials for the platform

## Usage

### Basic Usage

```python
from killer import killer
from utils.http_utils import get_task_list

# Get a task
tasks = get_task_list()
task = tasks[0]

# Generate and verify Litex solution
result = killer(task)
print(result)
# Returns: {"task_id": task["id"], "solution": "litex_code" or None}
```

### Batch Processing

```python
from utils.http_utils import get_task_list
from killer import killer

# Process multiple tasks
tasks = get_task_list(length=20)
for task in tasks:
    result = killer(task)
    if result['solution']:
        print(f"Task {result['task_id']} solved successfully")
    else:
        print(f"Task {result['task_id']} failed verification")
```

### Running Tests

```bash
# Basic functionality test
python test/basic_test.py

# Batch processing test
python test/batch_test.py
```

### Test Results

The batch test (`batch_test.py`) demonstrates the system's parallel processing capabilities:

- **Test Configuration**: 20 tasks processed with up to 100 parallel processes
- **Actual Performance Results**:
  - Total tasks processed: 20
  - Successful solutions: 18
  - Failed solutions: 2
  - **Success Rate**: 90% (18/20)

This test showcases the system's ability to handle multiple tasks concurrently while maintaining high accuracy using multiprocessing.

### Achieving 100% Success Rate

For users who require 100% success rate, you can run the `killer` function multiple times on failed tasks:

**Note**: Due to the non-deterministic nature of LLM responses, running the same task multiple times can yield different solutions, potentially solving previously failed tasks.

## Features

### Core Functionality

- **Automated Litex Code Generation**: Uses DeepSeek-R1 LLM for mathematical reasoning and Litex code generation
- **Example-Based Learning**: Learns from solved examples to improve solution quality
- **Code Verification**: Pylitex engine validates Litex code correctness
- **Robust Error Handling**: Comprehensive error handling for API failures and invalid solutions
- **Configurable Timeout**: 30-minute timeout (1800 seconds) for complex problems

### HTTP Utilities

- `get_task_list(length)`: Fetch tasks from Litex platform (default: 100 tasks)
- `get_example_list(length)`: Get solved examples for learning (default: 10 examples)

### Configuration Management

- Secure credential handling through `config.json`
- Template-based configuration with `config.json.temp`
- Git-ignored sensitive data protection
- Centralized configuration utilities in `utils/config_utils.py`

## Key Features

### Example-Based Learning
The system uses solved examples from the platform to improve solution quality. The `_prompt_generator()` function creates prompts that include relevant examples to guide the DeepSeek-R1 model.

### Fraction Handling
Automatically converts fractions to decimal numbers when possible for better computational accuracy.

### Litex Code Verification
All generated Litex code is verified using the Pylitex computational engine before being returned, ensuring mathematical correctness.

### Model Configuration
- **Model**: DeepSeek-R1 (deepseek-r1-250528)
- **Timeout**: 1800 seconds (30 minutes) for complex problems
- **Verification**: Pylitex engine validation

## Performance & Metrics

### Accuracy
- Pylitex verification ensures mathematical correctness of all returned Litex code
- Example-based learning improves solution quality over time
- Failed solutions are identified and can be logged for debugging

### Efficiency
- 30-minute timeout prevents infinite loops on complex problems
- Batch processing capability using multiprocessing for handling multiple tasks
- Optimized prompt generation using relevant examples

### Monitoring
- Solution success/failure tracking via `show_false_answers` parameter
- Debug output for failed solutions when `show_false_answers=True`
- Results returned for further processing or analysis

## API Reference

### `killer(row: dict, show_false_answers: bool = True) -> dict`

Main function that processes a single GSM8K problem using DeepSeek-R1 and Pylitex verification.

**Parameters:**
- `row`: Dictionary containing problem data with keys:
  - `id`: Problem identifier
  - `title`: Problem title
  - `description`: Problem statement
- `show_false_answers`: Whether to print failed solutions for debugging (default: True)

**Returns:**
- Dictionary with:
  - `task_id`: Problem identifier (same as `row["id"]`)
  - `solution`: Generated Litex code (or None if verification failed)

### HTTP Utilities

#### `get_task_list(length: int = 100) -> list[dict[str, str]]`
Fetches tasks from the Litex platform.

**Parameters:**
- `length`: Number of tasks to fetch (default: 100)

#### `get_example_list(length: int = 10) -> list[dict[str, str]]`
Retrieves solved examples for reference and learning.

**Parameters:**
- `length`: Number of examples to fetch (default: 10)

### Configuration Utilities

#### `load_config(config_filename: str = "config.json") -> Dict[str, Any]`
Load configuration from a JSON file.

#### `get_info(config_key: str, config_filename: str = "config.json") -> Dict[str, str]`
Get specific information from configuration file.

## Development

### Project Architecture

The project follows a modular architecture:
- `killer.py`: Core logic for Litex code generation and verification
- `utils/`: Utility modules for HTTP communication and configuration management
- `test/`: Test suites for validation and performance testing

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes
3. Add tests in `test/` directory
4. Update documentation
5. Submit pull request

### Testing

- Basic functionality test: `test/basic_test.py` - tests single task processing
- Batch processing test: `test/batch_test.py` - tests multiprocessing with 20 tasks and up to 100 parallel processes
- Integration tests with Litex platform API
- Litex code verification testing

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and returns
- Include docstrings for all public functions

## Security

- **Configuration**: `config.json` is git-ignored to protect sensitive data
- **API Keys**: Store securely and never commit to version control
- **Template**: Use `config.json.temp` for sharing configuration structure

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **API Authentication**: Verify API keys in `config.json`
   - Check VolcEngine API key is valid and has sufficient credits
   - Ensure Litex platform credentials are correct

3. **Network Issues**: Check internet connection and API endpoints
   - Test with a simple HTTP request to verify connectivity
   - Check firewall settings if running in restricted environments

4. **Pylitex Verification Failures**: Ensure generated Litex code is syntactically correct
   - Review failed solutions using `show_false_answers=True`
   - Check Litex code format matches expected Pylitex syntax

5. **Timeout Issues**: For very complex problems
   - Consider increasing timeout in the Ark client configuration
   - Break down complex problems into smaller steps

### Debug Mode

Enable verbose logging by modifying the killer function to include debug output, or use `show_false_answers=True` to print failed Litex code for analysis.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is part of the Litex platform ecosystem for mathematical problem solving and Litex code generation.

## Changelog

### Current Version
- DeepSeek-R1 model integration for advanced mathematical reasoning and Litex code generation
- Example-based learning system for improved solution quality
- Robust Pylitex verification engine integration
- Comprehensive error handling and debugging features
- Modular architecture with utilities for HTTP and configuration management

### Features Added
- Automatic fraction to decimal conversion
- Configurable timeout (1800 seconds) for complex problems
- Debug mode for failed solution analysis using `show_false_answers` parameter
- Template-based configuration system
- Multiprocessing support for batch processing

## Support

For issues and questions:
- Check the troubleshooting section
- Review test files for usage examples
- Contact the development team through the Litex platform
