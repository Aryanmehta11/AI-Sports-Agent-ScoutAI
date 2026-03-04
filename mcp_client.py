import json
import asyncio

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession


async def call_mcp_tool(tool_name, args):

    with open("mcp.json") as f:
        config = json.load(f)

    server_config = list(config["mcpServers"].values())[0]

    server = StdioServerParameters(
        command=server_config["command"],
        args=server_config["args"]
    )

    async with stdio_client(server) as (read, write):

        async with ClientSession(read, write) as session:

            result = await session.call_tool(tool_name, args)

            return result