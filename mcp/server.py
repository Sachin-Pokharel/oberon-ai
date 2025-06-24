from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv("../.env")

mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0", # only used ofr SSE transport (localhost)
    port=8050, # only used for SSE transport
)

# Add a simple calculator
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers together."""
    return a + b


# In production use this allow from env variable
if __name__ == "__main__":
    transport = "streamable-http"  # Default transport
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    elif transport == "streamable-http":
        print("Running server with streamable HTTP transport")
        mcp.run(transport="streamable-http")
    else:
        raise ValueError(f"Unknown transport: {transport}")