# MCP-Server

uvicorn src.server:app --reload

# Parquet data:
{
  "jsonrpc": "2.0",
  "method": "mcp/callTool",
  "id": 2,
  "params": {
    "tool": "parquet",
    "column": "temperature"
  }
}

# Sorting Log data
{
    "jsonrpc": "2.0",
    "method": "mcp/callTool",
    "params": {
        "tool": "sort",
        "file": "huge_log.txt"
    },
    "id": 1
}

{
    "jsonrpc": "2.0",
    "method": "mcp/callTool",
    "params": {
        "tool": "sort",
        "file": "small_log.txt"
    },
    "id": 1
}

# Processing CSV using pandas:
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