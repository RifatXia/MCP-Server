# MCP Server Implementation

## Student Information
- Name: Zia Uddin Chowdhury
- Student ID: A20615319

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
    "pytest-asyncio==0.26.0",
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

## JSON-RPC Requests and Responses

### 1. List Available Tools

Request:
```json
{
    "jsonrpc": "2.0",
    "method": "mcp/listTools",
    "id": 1
}
```

Response:
```json
{
    "jsonrpc": "2.0",
    "result": [
        {
            "id": "tool1",
            "name": "Parquet Reader",
            "description": "Reads columns from Parquet files",
            "usage": "'tool': 'parquet', 'file': 'filename (optional)', 'column': 'column_name' in params."
        },
        {
            "id": "tool2",
            "name": "Parallel Sorting",
            "description": "Sorts log file entries by timestamp",
            "usage": "'tool': 'sort', 'file': 'log_filename' in params."
        },
        {
            "id": "tool3",
            "name": "Compression Tool",
            "description": "Compresses files using gzip",
            "usage": "'tool': 'compress', 'file': 'filename' in params."
        },
        {
            "id": "tool4",
            "name": "Data Analysis using Pandas",
            "description": "Analyzes CSV files using pandas",
            "usage": "'tool': 'pandas', 'file': 'filename', 'column': 'column_name', 'threshold': value in params."
        }
    ],
    "id": 1
}
```

### 2. Read Parquet Data

Request:
```json
{
    "jsonrpc": "2.0",
    "method": "mcp/callTool",
    "params": {
        "tool": "parquet",
        "column": "temperature"
    },
    "id": 2
}
```

Response:
```json
{
    "jsonrpc": "2.0",
    "id": 2,
    "result": [
        14.96,
        2.01,
        0.56,
        16.19,
        30.18,
        "..."
    ]
}
```

### 3. Sort Log Data

#### Example 1: Small Log File

Request:
```json
{
    "jsonrpc": "2.0",
    "method": "mcp/callTool",
    "params": {
        "tool": "sort",
        "file": "small_log.txt"
    },
    "id": 1
}
```

Response:
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": [
        "2024-03-15 09:15:22 WARNING High CPU usage detected",
        "2024-03-15 09:30:55 WARNING Network latency increased",
        "2024-03-15 10:30:45 INFO Server started successfully",
        "2024-03-15 11:00:45 INFO Scheduled maintenance started"
    ]
}
```

#### Example 2: Large Log File

Request:
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

Response:
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": [
        "2024-03-15 09:00:00 INFO System initialization complete",
        "2024-03-15 09:15:22 WARNING High CPU usage detected",
        "2024-03-15 09:30:55 WARNING Network latency increased",
        "2024-03-15 09:45:18 INFO User authentication successful",
        "2024-03-15 10:00:15 INFO Backup process started",
        "2024-03-15 10:15:33 ERROR File system error detected",
        "2024-03-15 10:30:45 INFO Server started successfully",
        "2024-03-15 11:00:45 INFO Scheduled maintenance started",
        "2024-03-15 11:30:00 WARNING Memory usage above 80%",
        "2024-03-15 11:45:30 ERROR Database connection failed"
    ]
}
```

### 4. Compress File

Request:
```json
{
    "jsonrpc": "2.0",
    "method": "mcp/callTool",
    "params": {
        "tool": "compress",
        "file": "output.log"
    },
    "id": 1
}
```

Response:
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "status": "success",
        "original_file": "data/output.log",
        "compressed_file": "data/output.log.gz",
        "original_size": 603,
        "compressed_size": 337,
        "compression_ratio": "44.11%"
    }
}
```

### 5. Process CSV Data

Request:
```json
{
    "jsonrpc": "2.0",
    "method": "mcp/callTool",
    "params": {
        "tool": "pandas",
        "file": "data.csv",
        "column": "marks",
        "threshold": 95
    },
    "id": 1
}
```

Response:
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "status": "success",
        "total_rows": 75,
        "filtered_rows": 4,
        "data": [
            {
                "id": 29,
                "name": "Jordan Thomas",
                "subject": "Science",
                "marks": 100
            },
            {
                "id": 32,
                "name": "Jamie Thomas",
                "subject": "Science",
                "marks": 97
            },
            "..."
        ]
    }
}
```