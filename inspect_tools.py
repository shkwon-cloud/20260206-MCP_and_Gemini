
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:8002/sse") as client:
        tools = await client.list_tools()
        for tool in tools:
            print(f"Name: {tool.name}")
            print(f"Description: {tool.description}")
            print(f"Input Schema: {tool.inputSchema}")
            print("-" * 20)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
