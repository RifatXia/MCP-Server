from fastapi import HTTPException
import os
from src.capabilities.parquet_handler import read_column
from src.capabilities.sort_handler import sort_log_by_timestamp
from src.capabilities.compression_handler import compress_file
from src.capabilities.pandas_handler import analyze_csv

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
             
        # read column data from parquet file
        result = read_column(filepath, column)   
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    
    elif tool == "sort":
        file = params.get("file", "huge_log.txt")
        filepath = os.path.join("data", file)
        
        # sort log file by timestamp
        result = sort_log_by_timestamp(filepath)
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    
    elif tool == "compress":
        file = params.get("file", "output.log")
        filepath = os.path.join("data", file)
        
        # compress file using gzip
        result = compress_file(filepath)
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    
    elif tool == "pandas":
        file = params.get("file", "data.csv")
        column = params.get("column", "marks")
        threshold = params.get("threshold", 50)
        
        filepath = os.path.join("data", file)
        
        # analyze csv data using pandas
        result = analyze_csv(filepath, column, threshold)
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    
    else:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Tool not found"},
            "id": request_id
        }
