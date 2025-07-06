import asyncio
from typing import Optional
from typing import Any, Dict, List, Optional
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import AsyncOpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = AsyncOpenAI(api_key=api_key)

    async def connect_to_streamable_http_server(
        self, server_url: str, headers: Optional[dict] = None
    ):
        self._streams_context = streamablehttp_client(
            url=server_url, headers=headers or {}
        )
        read_stream, write_stream, _ = await self._streams_context.__aenter__()
        self._session_context = ClientSession(read_stream, write_stream)
        self.session: ClientSession = await self._session_context.__aenter__()

        await self.session.initialize()

    async def get_mcp_tools(self) -> List[Dict[str, Any]]:
        """Get available tools from the MCP server in OpenAI format.

        Returns:
            A list of tools in OpenAI format.
        """
        tools_result = await self.session.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in tools_result.tools
        ]

    async def process_query(self, query: str) -> str:
        """Process a query using OpenAI and available MCP tools.

        Args:
            query: The user query.

        Returns:
            The response from OpenAI.
        """
        # Get available tools
        tools = await self.get_mcp_tools()

        print(f"Using tools: {tools}")

        # Initial OpenAI API call
        response = await self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": query}],
            tools=tools,
            tool_choice="auto",
        )

        # Get assistant's response
        assistant_message = response.choices[0].message
        
        # Initialize conversation with user query and assistant response
        messages = [
            {"role": "user", "content": query},
            assistant_message,
        ]

        # Handle tool calls if present
        if assistant_message.tool_calls:
            # Process each tool call
            for tool_call in assistant_message.tool_calls:
                # Execute tool call
                result = await self.session.call_tool(
                    tool_call.function.name,
                    arguments=json.loads(tool_call.function.arguments),
                )
                
                # Add tool response to conversation
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result.content[0].text,
                    }
                )

            # Get final response from OpenAI with tool results
            final_response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
                tool_choice="none",  # Don't allow more tool calls
            )

            # Return the content of the final assistant message, not just the content string
            return final_response.choices[0].message.content

        # No tool calls, just return the direct response
        return assistant_message.content

    async def chat_loop(self):
        print("Connected to MCP server. You can start chatting!")
        # List available tools
        tools_result = await self.session.list_tools()
        print("\nConnected to server with tools:")
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    break
                response = await self.process_query(user_input)
                print(f"Bot: {response}")
            except Exception as e:
                print(f"Error: {e}")

    async def cleanup(self):
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)


async def main():
    client = MCPClient()
    try:
        await client.connect_to_streamable_http_server(
            f"http://localhost:8123/mcp")
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
