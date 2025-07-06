import argparse
import uvicorn
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.get_weather import get_weather_from_api
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="oberon-ai",
    json_reponse=False,
    stateless_http=False
)

@mcp.tool()
def weather(query: str) -> dict:
    """
    MCP tool to get weather information for a given location query.
    """
    return get_weather_from_api(query)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MCP Streamable HTTP based server")
    parser.add_argument("--port", type=int, default=8123, help="Localhost port to listen on")
    args = parser.parse_args()
    # Start the server with Streamable HTTP transport
    uvicorn.run(mcp.streamable_http_app, host="localhost", port=args.port)
