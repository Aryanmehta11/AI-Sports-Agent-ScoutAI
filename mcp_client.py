import json
import asyncio
import sys

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

# ✅ CRITICAL FIX for Windows: use ProactorEventLoop for subprocess support
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


async def call_mcp_tool(tool_name: str, args: dict):

    with open("mcp.json") as f:
        config = json.load(f)

    server_config = list(config["mcpServers"].values())[0]

    server = StdioServerParameters(
        command=server_config["command"],
        args=server_config["args"],
        env=None
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:

            # ✅ CRITICAL FIX: Must initialize session before calling any tools
            await session.initialize()

            result = await session.call_tool(tool_name, args)
            return result