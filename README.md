# MCP Server Implementation

## Student Information
- Name: Zia Uddin Chowdhury
- Student ID: 20615319

## Implemented MCP Capabilities

1. **Parquet Handler**
   - Reads columns from Parquet files
   - Supports error handling for non-existent files and columns

2. **Sort Handler**
   - Sorts log file entries by timestamp
   - Handles empty files and invalid formats

3. **Compression Handler**
   - Compresses files using gzip
   - Provides compression statistics (original size, compressed size, ratio)

4. **Pandas Handler**
   - Analyzes CSV files
   - Filters data based on column values and thresholds

## Environment Setup (Linux)

1. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install and use uv for dependency management:
```bash
# Install uv
pip install uv

# Install dependencies from pyproject.toml
uv pip install --requirement pyproject.toml
```

Dependencies are specified in pyproject.toml:
```toml
[project]
name = "mcp_server"
version = "0.1.0"
dependencies = [
    "fastapi>=0.115.12",
    "numpy>=2.2.4",
    "pandas>=2.2.3",
    "pyarrow>=19.0.1",
    "pydantic>=2.11.3",
    "pytest>=8.3.5",
    "requests>=2.32.3",
    "uvicorn>=0.34.1",
]

python = ">=3.10"
```

## Running the MCP Server

1. Ensure you're in the virtual environment
2. Start the server:
```bash
python3 src/server.py
```

The server will start on `localhost:8000` by default.

## Running Tests

Run all tests:
```bash
python3 -m pytest
```

Run specific test files:
```bash
python3 -m pytest tests/test_sort_handler.py
python3 -m pytest tests/test_parquet_handler.py
python3 -m pytest tests/test_compression_handler.py
python3 -m pytest tests/test_pandas_handler.py
```

## Implementation Notes

1. **Sort Handler**
   - Expects log files with timestamp format: "YYYY-MM-DD HH:MM:SS"
   - Returns sorted lines or error message for invalid formats

2. **Compression Handler**
   - Creates .gz files in the same directory as the input file
   - Empty files will result in an error due to compression ratio calculation
   - Original files are preserved

3. **Parquet Handler**
   - Requires pyarrow installation
   - Supports reading single columns from parquet files

4. **Pandas Handler**
   - Expects CSV files with headers
   - Supports filtering based on numeric thresholds
   - Returns filtered data in dictionary format

## Project Structure
```
MCP-Server/
├── src/
│   ├── capabilities/
│   │   ├── __init__.py
│   │   ├── compression_handler.py
│   │   ├── pandas_handler.py
│   │   ├── parquet_handler.py
│   │   └── sort_handler.py
│   ├── __init__.py
│   ├── mcp_handlers.py
|   └── server.py
├── tests/
│   ├── __init__.py
│   ├── test_compression_handler.py
│   ├── test_pandas_handler.py
│   ├── test_parquet_handler.py
│   └── test_sort_handler.py
├── data/
├── README.md
├── pyproject.toml
└── pytest.ini
```

## Example JSON-RPC Requests

1. Read Parquet Data:
```json
{
  "jsonrpc": "2.0",
  "method": "mcp/callTool",
  "id": 2,
  "params": {
    "tool": "parquet",
    "column": "temperature"
  }
}
```

2. Sort Log Data:
```json
{
    "jsonrpc": "2.0",
    "method": "mcp/callTool",
    "params": {
        "tool": "sort",
        "file": "huge_log.txt"
    },
    "id": 1
}
```

3. Process CSV Data:
```json
{
    "jsonrpc": "2.0",
    "method": "mcp/callTool",
    "params": {
        "tool": "pandas",
        "file": "data.csv",
        "column": "marks",
        "threshold": 0
    },
    "id": 1
}
```