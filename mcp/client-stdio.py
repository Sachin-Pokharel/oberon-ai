import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import nest_asyncio

nest_asyncio.apply()  # Apply nest_asyncio to allow nested event loops


async def main():
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],  # Adjust the path to your server script
    )
    
    # Connect to the server
    async with stdio_client(server_params) as (read_stream, write_stream):
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
            print(f"2 + 3 = {add_result.content[0].text}")
            
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

            
        