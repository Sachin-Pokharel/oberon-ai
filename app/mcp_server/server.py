import argparse
import uvicorn
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="oberon-ai",
    json_reponse=False,
    stateless_http=False
)

# Add a simple calculator
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers together."""
    return a + b


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MCP Streamable HTTP based server")
    parser.add_argument("--port", type=int, default=8123, help="Localhost port to listen on")
    args = parser.parse_args()
    # Start the server with Streamable HTTP transport
    uvicorn.run(mcp.streamable_http_app, host="localhost", port=args.port)