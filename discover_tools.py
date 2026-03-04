"""
Test every major tool category to understand what data each returns.
Run: python discover_tools.py
"""
import asyncio, sys, json
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from mcp_client import call_mcp_tool

async def test(label, tool, args):
    print(f"\n{'='*60}")
    print(f"TOOL: {tool}  |  args: {args}")
    print(f"{'='*60}")
    try:
        r = await call_mcp_tool(tool, args)
        data = json.loads(r.content[0].text)
        status = data.get("status")
        print(f"Status: {status}")
        resp = data.get("response", data)
        # Print first item or first 600 chars to understand schema
        if isinstance(resp, list) and resp:
            print(json.dumps(resp[0], indent=2)[:600])
        elif isinstance(resp, dict):
            for k, v in list(resp.items())[:3]:
                val = v[0] if isinstance(v, list) and v else v
                print(f"  '{k}': {json.dumps(val, indent=2)[:300]}")
        else:
            print(str(resp)[:600])
    except Exception as e:
        print(f"ERROR: {e}")

async def main():
    PL = 47  # Premier League

    await test("Top Scorers PL",       "Get_Top_Players_by_Goals",    {"leagueId": PL})
    await test("Top Assists PL",       "Get_Top_Players_by_Assists",  {"leagueId": PL})
    await test("Top Rated PL",         "Get_Top_Players_by_Rating",   {"leagueId": PL})
    await test("PL Standings",         "Get_Standing_All_by_League_ID", {"leagueId": PL})
    await test("PL Matches",           "Get_All_MatchesEvents_by_League_ID", {"leagueId": PL})
    await test("Transfers Top",        "Get_Top_Transfers",           {})
    await test("Transfers PL",         "Get_Transfers_by_League_ID",  {"leagueId": PL})
    await test("Trending News",        "Get_Trending_News",           {})
    await test("News PL",              "Get_News_League_by_League_ID",{"leagueId": PL})
    await test("Search Player Salah",  "Get_Search_All_Players",      {"query": "Salah"})
    await test("Search Team Arsenal",  "Get_Search_Teams",            {"query": "Arsenal"})
    await test("Live Scores",          "Get_LivescoresMatchesEvents", {})

asyncio.run(main())