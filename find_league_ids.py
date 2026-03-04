"""
Deep inspection - prints raw response to understand the real data structure
"""
import asyncio, sys, json
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from mcp_client import call_mcp_tool

async def main():

    # ── Try 1: Get_Popular_Leagues (simpler endpoint, likely has clean IDs) ──
    print("=" * 60)
    print("TEST 1: Get_Popular_Leagues")
    print("=" * 60)
    result = await call_mcp_tool("Get_Popular_Leagues", {})
    raw = json.loads(result.content[0].text)
    print(json.dumps(raw, indent=2)[:3000])

    # ── Try 2: Search for Premier League directly ────────────────────────────
    print("\n" + "=" * 60)
    print("TEST 2: Get_Search_Leagues  query='Premier League'")
    print("=" * 60)
    result2 = await call_mcp_tool("Get_Search_Leagues", {"query": "Premier League"})
    raw2 = json.loads(result2.content[0].text)
    print(json.dumps(raw2, indent=2)[:3000])

    # ── Try 3: Print the FULL raw structure of Leagues_List_All ─────────────
    print("\n" + "=" * 60)
    print("TEST 3: Get_Leagues_List_All — first 2 items raw")
    print("=" * 60)
    result3 = await call_mcp_tool("Get_Leagues_List_All", {})
    raw3 = json.loads(result3.content[0].text)
    # Print just first 2 items so we can see the real schema
    top_level_keys = list(raw3.keys())
    print("Top-level keys:", top_level_keys)
    response = raw3.get("response", raw3)
    if isinstance(response, list):
        print("First 2 items:")
        print(json.dumps(response[:2], indent=2))
    elif isinstance(response, dict):
        for k, v in response.items():
            print(f"Key '{k}':", str(v)[:200])

asyncio.run(main())