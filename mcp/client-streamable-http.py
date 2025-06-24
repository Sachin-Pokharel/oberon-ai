import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

nest_asyncio.apply()  # Needed if you're running in Jupyter or Streamlit

async def main():
    # Connect using streamable HTTP client
    async with streamablehttp_client("http://localhost:8050/mcp") as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the MCP session
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")

            # Call a tool (e.g., "add")
            result = await session.call_tool("add", arguments={"a": 10, "b": 7})
            print(f"10 + 7 = {result.content[0].text}")

# Run
if __name__ == "__main__":
    asyncio.run(main())
