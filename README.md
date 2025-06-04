# MCP Agent Demo

A powerful demonstration of a Multi-Component Protocol (MCP) agent system that showcases various data processing and analysis capabilities.

## Features

- FastAPI-based server implementation
- Multiple built-in tools for data processing
- JSON formatting and validation
- Text analysis and information extraction
- Data validation and transformation
- Error handling and status reporting
- API key authentication

## Project Structure

```plaintext
mcp-agent-demo/
├── mcp/
│   ├── core/
│   │   ├── config.py        # Configuration management
│   │   └── server.py        # Base server implementation
│   └── agents/
│       ├── __init__.py
│       └── demo_agent.py    # Enhanced demo agent implementation
├── .env                     # Environment variables
├── pyproject.toml          # Project dependencies
├── setup.py               # Package installation
├── run.py                # One-command setup and run script
└── README.md             # This file
```

## Quick Start

### Option 1: One-Command Setup and Run

Simply run:

```bash
python run.py
```

This will:

1. Check Python version (requires 3.9+)
2. Create a virtual environment if needed
3. Install all dependencies
4. Start the MCP Agent

### Option 2: Manual Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate  # On Windows
source .venv/bin/activate      # On Unix/MacOS
```

2.Install dependencies:

```bash
pip install -e .
```

3.Start the demo agent:

```bash
python -m mcp.agents.demo_agent
```

## Available Tools

The demo agent provides several powerful tools for data processing and analysis:

### 1. Echo Tool

Echoes back input data with timestamp.

```bash
curl -X POST http://localhost:8000/tools/echo \
  -H "X-API-Key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, World!"}'
```

### 2. Calculate Tool

Performs various mathematical operations.

```bash
curl -X POST http://localhost:8000/tools/calculate \
  -H "X-API-Key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "power",
    "a": 2,
    "b": 3
  }'
```

Supported operations: add, subtract, multiply, divide, power, sqrt

### 3. Analyze Text Tool

Provides detailed text analysis and statistics.

```bash
curl -X POST http://localhost:8000/tools/analyze_text \
  -H "X-API-Key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a sample text. It has multiple sentences. And some paragraphs."
  }'
```

Returns: character count, word count, unique words, sentence count, paragraph count, averages, and more.

### 4. Format JSON Tool

Formats and validates JSON data.

```bash
curl -X POST http://localhost:8000/tools/format_json \
  -H "X-API-Key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "json_string": "{\"name\":\"John\",\"age\":30}",
    "indent": 2
  }'
```

### 5. Extract Info Tool

Extracts specific information from text using patterns.

```bash
curl -X POST http://localhost:8000/tools/extract_info \
  -H "X-API-Key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Contact us at john@example.com or call 123-456-7890",
    "patterns": {
      "email": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
    }
  }'
```

Default patterns: email, phone, URL

### 6. Validate Data Tool

Validates data against custom rules.

```bash
curl -X POST http://localhost:8000/tools/validate_data \
  -H "X-API-Key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "John",
      "age": 30
    },
    "rules": {
      "name": {
        "required": true,
        "min_length": 2
      },
      "age": {
        "type": "int",
        "min_length": 1
      }
    }
  }'
```

### 7. Transform Data Tool

Transforms data using various operations.

```bash
curl -X POST http://localhost:8000/tools/transform_data \
  -H "X-API-Key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "john",
      "age": "30"
    },
    "transformations": [
      {
        "operation": "convert",
        "field": "age",
        "type": "int"
      },
      {
        "operation": "set",
        "field": "status",
        "value": "active"
      }
    ]
  }'
```

Supported operations: set, delete, rename, convert

## Response Format

All tools return responses in a consistent format:

```json
{
  "status": "success|error",
  "data": { ... },
  "error": "Error message if status is error"
}
```

## Configuration

The agent can be configured using environment variables or a `.env` file:

```env
DEMO_AGENT_PORT=8000
DEMO_AGENT_API_KEY=demo-secret-key
LOG_LEVEL=INFO
```

## Error Handling

The agent includes comprehensive error handling:

- Invalid API keys return 401 Unauthorized
- Invalid tool names return 404 Not Found
- Tool execution errors return 500 Internal Server Error
- All errors include descriptive messages

## Security

- API key authentication required for all endpoints
- Input validation for all tools
- Safe execution environment for transformations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
