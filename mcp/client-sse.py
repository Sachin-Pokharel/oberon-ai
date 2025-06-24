import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()  # Apply nest_asyncio to allow nested event loops

"""
Make sure:
1. The server is running before you run this client.
2. The server is configured to use SSE transport.
3. The server is listening on the correct host and port (default is 8050). 
To run the server, use:
uv run server.py
"""

async def main():
    # Connect to the server using SSE
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")
                
            # Call the 'add' tool
            add_result = await session.call_tool("add", arguments={"a": 5, "b": 3})
            print(f"5 + 3 = {add_result.content[0].text}")  
            

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())