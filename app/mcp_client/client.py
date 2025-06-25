import argparse
import asyncio
from openai import OpenAI
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

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
        
    async def process_query(self, query: str) -> str:
        return query


    async def chat_loop(self):
        print("Connected to MCP server. You can start chatting!")
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