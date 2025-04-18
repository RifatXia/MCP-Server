from fastapi import HTTPException

# sample data for resources
resources = [
    {"id": "resource1", "type": "HDF5", "description": "Sample HDF5 resource"},
    {"id": "resource2", "type": "S3", "description": "Sample S3 resource"}
]

# sample data for tools
tools = [
    {"id": "tool1", "name": "Compression Tool", "description": "Simulates data compression"},
    {"id": "tool2", "name": "Slurm Job Scheduler", "description": "Simulates job scheduling"}
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
        return call_tool(params)
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
def call_tool(params):
    tool_id = params.get("tool_id")
    if not tool_id:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32602, "message": "Invalid params"},
            "id": None
        }

    # simulate tool execution
    if tool_id == "tool1":
        result = "Data compressed successfully"
    elif tool_id == "tool2":
        result = "Job submitted successfully"
    else:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Tool not found"},
            "id": None
        }

    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": None
    } 