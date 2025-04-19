# MCP-Server

uvicorn src.server:app --reload

Parquet data:
{
  "jsonrpc": "2.0",
  "method": "mcp/callTool",
  "id": 2,
  "params": {
    "tool": "parquet",
    "column": "temperature"
  }
}
