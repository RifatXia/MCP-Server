from fastapi import HTTPException
import os
from src.capabilities.parquet_handler import read_column

# sample data for resources
resources = [
    {"id": "resource1", "type": "HDF5", "description": "Sample HDF5 resource"},
    {"id": "resource2", "type": "S3", "description": "Sample S3 resource"}
]

# handle mcp request
def handle_mcp_request(data):
    if "jsonrpc" not in data or "method" not in data:
        raise HTTPException(status_code=400, detail="Invalid JSON-RPC request")

    method = data["method"]
    params = data.get("params", {})

    if method == "mcp/listResources":
        return list_resources()
    elif method == "mcp/callTool":
        return call_tool(params, data.get("id"))
    else:
        raise HTTPException(status_code=400, detail="Method not supported")

# list available resources
def list_resources():
    return {
        "jsonrpc": "2.0",
        "result": resources,
        "id": None
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
