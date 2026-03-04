import asyncio
import sys

# ✅ Must be set BEFORE any asyncio.run() call on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from mcp_client import call_mcp_tool


async def main():

    print("Testing MCP connection...\n")

    # Step 1: List all available tools so you know the exact names
    print("--- Discovering available tools ---")
    from mcp.client.stdio import stdio_client, StdioServerParameters
    from mcp import ClientSession
    import json

    with open("mcp.json") as f:
        config = json.load(f)
    server_config = list(config["mcpServers"].values())[0]
    server = StdioServerParameters(
        command=server_config["command"],
        args=server_config["args"],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"✅ Found {len(tools.tools)} tools:\n")
            for t in tools.tools:
                print(f"  - {t.name}: {t.description[:60] if t.description else 'no description'}...")

    # Step 2: Call the first available tool as a live test
    print("\n--- Calling first tool as live test ---")
    if tools.tools:
        first_tool = tools.tools[0].name
        print(f"Calling: {first_tool}")
        data = await call_mcp_tool(first_tool, {})
        print(f"✅ Response received:")
        print(str(data)[:500])


if __name__ == "__main__":
    asyncio.run(main())