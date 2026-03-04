# tool_router.py — Only routes to tools that ACTUALLY WORK on this API

def build_tool_call(context: dict) -> tuple[str, dict]:
    intent    = context.get("intent", "trending_news")
    league_id = context.get("league_id") or 47

    # ── WORKS: Trending news (best for viral content) ─────────────────────────
    if intent == "trending_news":
        return "Get_Trending_News", {}

    # ── WORKS: League-specific news ───────────────────────────────────────────
    elif intent == "news_league":
        return "Get_News_League_by_League_ID", {"leagueId": league_id}

    # ── WORKS: Transfers (great content — who moved, fees, clubs) ─────────────
    elif intent == "transfers":
        return "Get_Top_Transfers", {}

    # ── WORKS: Live scores ────────────────────────────────────────────────────
    elif intent == "livescores":
        return "Get_LivescoresMatchesEvents", {}

    # ── WORKS: Fixtures by league (may be empty off-season) ───────────────────
    elif intent == "league_matches":
        return "Get_All_MatchesEvents_by_League_ID", {"leagueId": league_id}

    # ── FALLBACK: Everything else → trending news (safe default) ─────────────
    # standings, top_goals, top_assists, player_search etc. all fail on this API
    else:
        print(f"⚠️  Intent '{intent}' not supported by this API → falling back to trending news")
        return "Get_Trending_News", {}