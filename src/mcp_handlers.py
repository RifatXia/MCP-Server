from fastapi import HTTPException
import os
from src.capabilities.parquet_handler import read_column

# sample data for resources
resources = [
    {"id": "resource1", "type": "Parquet", "description": "Sample Parquet resource"}
]

tools = [
    {
        "id": "tool1",
        "name": "Parquet Reader",
        "description": "Reads columns from Parquet files",
        "usage": "'tool': 'parquet', 'file': 'filename (optional)', 'column': 'column_name' in params."
    }
]

# handle mcp request
def handle_mcp_request(data):
    if "jsonrpc" not in data or "method" not in data:
        raise HTTPException(status_code=400, detail="Invalid JSON-RPC request")

    method = data["method"]
    params = data.get("params", {})

    if method == "mcp/listResources":
        return list_resources(data.get("id"))
    elif method == "mcp/listTools":
        return list_tools(data.get("id"))
    elif method == "mcp/callTool":
        return call_tool(params, data.get("id"))
    else:
        raise HTTPException(status_code=400, detail="Method not supported")

# list available resources
def list_resources(id):
    return {
        "jsonrpc": "2.0",
        "result": resources,
        "id": id
    }

# list of available tools
def list_tools(id):
    return {
        "jsonrpc": "2.0",
        "result": tools,
        "id": id
    }

# execute tool based on id
def call_tool(params, request_id):
    tool = params.get("tool")
    if not tool:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32602, "message": "Invalid params"},
            "id": request_id
        }

    if tool == "parquet":
        file = params.get("file", "weather_data.parquet")
        column = params.get("column")
        
        filepath = os.path.join("data", file)
             
        # read the column data
        result = read_column(filepath, column)   
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    else:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Tool not found"},
            "id": request_id
        }
