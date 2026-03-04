import asyncio
import json

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession


async def main():

    with open("mcp.json", "r") as f:
        config = json.load(f)

    server_config = list(config["mcpServers"].values())[0]

    server = StdioServerParameters(
        command=server_config["command"],
        args=server_config["args"]
    )

    async with stdio_client(server) as (read, write):

        async with ClientSession(read, write) as session:

            tools = await session.list_tools()

            print("\nAvailable MCP Tools:\n")

            for tool in tools:
                print(tool)   # <-- changed here


asyncio.run(main())