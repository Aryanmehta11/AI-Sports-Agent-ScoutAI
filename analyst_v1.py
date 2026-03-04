# agent.py — Sports Content Creator Agent  v3
# ════════════════════════════════════════════════════════════════
# Built around 5 tools that ACTUALLY WORK on this API:
#   Get_Trending_News
#   Get_News_League_by_League_ID
#   Get_Top_Transfers
#   Get_LivescoresMatchesEvents
#   Get_All_MatchesEvents_by_League_ID
# ════════════════════════════════════════════════════════════════

import json, asyncio, sys
from datetime import datetime
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

from prompts import context_prompt, analysis_prompt, content_prompt
from mcp_client import call_mcp_tool
from tool_router import build_tool_call

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)


class AgentState(TypedDict):
    question:   str
    context:    dict
    tool_used:  str
    data:       dict
    analysis:   str
    content:    str


# ── Node 1: Extract Context ───────────────────────────────────────────────────
def extract_context(state: AgentState) -> dict:
    today  = datetime.now().strftime("%Y-%m-%d")
    prompt = context_prompt.format(today=today) + f"\n\nQuestion: {state['question']}"
    res    = llm.invoke(prompt)
    try:
        raw     = res.content.strip().strip("```json").strip("```").strip()
        context = json.loads(raw)
    except Exception as e:
        print(f"⚠️  Parse failed ({e}) — defaulting to trending_news")
        context = {"intent": "trending_news"}
    print(f"🧠 Intent: {context.get('intent')}  |  league_id: {context.get('league_id')}")
    return {"context": context}


# ── Node 2: Route + Fetch ─────────────────────────────────────────────────────
def route_and_fetch(state: AgentState) -> dict:
    tool_name, args = build_tool_call(state["context"])
    print(f"📡 Tool: {tool_name}  |  Args: {args}")
    raw = asyncio.run(call_mcp_tool(tool_name, args))
    try:
        data = json.loads(raw.content[0].text)
    except Exception:
        data = {"raw": str(raw)}
    if data.get("status") == "failed":
        print(f"⚠️  API failed: {data.get('message')} — falling back to trending news")
        fallback = asyncio.run(call_mcp_tool("Get_Trending_News", {}))
        try:
            data = json.loads(fallback.content[0].text)
            tool_name = "Get_Trending_News (fallback)"
        except Exception:
            pass
    return {"tool_used": tool_name, "data": data}


# ── Node 3: Analyze ───────────────────────────────────────────────────────────
def analyze(state: AgentState) -> dict:
    data_str = json.dumps(state["data"], indent=2)
    if len(data_str) > 12_000:
        data_str = data_str[:12_000] + "\n... [truncated]"
    prompt = analysis_prompt.format(question=state["question"], data=data_str)
    res    = llm.invoke(prompt)
    return {"analysis": res.content}


# ── Node 4: Generate Content ──────────────────────────────────────────────────
def generate_content(state: AgentState) -> dict:
    res = llm.invoke(content_prompt.format(analysis=state["analysis"]))
    return {"content": res.content}


# ── Graph ─────────────────────────────────────────────────────────────────────
builder = StateGraph(AgentState)
builder.add_node("extract_context",  extract_context)
builder.add_node("route_and_fetch",  route_and_fetch)
builder.add_node("analyze",          analyze)
builder.add_node("generate_content", generate_content)
builder.set_entry_point("extract_context")
builder.add_edge("extract_context",  "route_and_fetch")
builder.add_edge("route_and_fetch",  "analyze")
builder.add_edge("analyze",          "generate_content")
builder.add_edge("generate_content", END)
app = builder.compile()


# ── CLI ───────────────────────────────────────────────────────────────────────
QUESTIONS = [
    "What are the biggest transfers right now?",
    "Give me the latest Premier League news",
    "What's trending in football today?",
    "Give me Champions League news",
    "Any football news today?",
]

if __name__ == "__main__":
    print("\n⚽  Sports Content Creator Agent  v3")
    print("─" * 45)
    print("✅ Questions that work with this API:")
    for i, q in enumerate(QUESTIONS, 1):
        print(f"  {i}. {q}")
    print()

    question = input("Ask a sports question: ").strip()

    result = app.invoke({
        "question":  question,
        "context":   {},
        "tool_used": "",
        "data":      {},
        "analysis":  "",
        "content":   "",
    })

    print(f"\n🔧 Tool used: {result['tool_used']}")
    print("\n" + "═" * 55)
    print("  ANALYSIS")
    print("═" * 55)
    print(result["analysis"])
    print("\n" + "═" * 55)
    print("  YOUR CONTENT")
    print("═" * 55)
    print(result["content"])