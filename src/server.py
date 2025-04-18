from fastapi import FastAPI, Request
from .mcp_handlers import handle_mcp_request

app = FastAPI()

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    data = await request.json()
    return handle_mcp_request(data)
