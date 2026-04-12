# ⚽ ScoutAI — Agentic Sports Content Engine

> An AI Agent that fetches live football data, analyses it, and generates ready-to-post YouTube Shorts scripts and Instagram captions — in under 60 seconds.

## 🎯 The Problem

Sports content creators spend **3–4 hours** manually:
- Digging through transfer news and match reports
- Finding a unique angle nobody else has posted
- Writing scripts, captions, and hooks from scratch

**ScoutAI cuts that to under 60 seconds.**

---

## 🤖 What Makes This an AI Agent

This is not a chatbot. Not a prompt wrapper. It's a real decision-making pipeline.

```
You type one question
        │
        ▼
┌─────────────────────┐
│   extract_context   │  Gemini reads your question
│     (LLM Node)      │  outputs structured JSON intent
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   route_and_fetch   │  Picks the right tool from the tested football MCP tools
│    (Logic Node)     │  Calls RapidAPI via MCP protocol
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      analyze        │  Gemini reads raw API data
│     (LLM Node)      │  Writes expert analysis with real stats
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  generate_content   │  Gemini writes viral content
│     (LLM Node)      │  Titles + Hooks + Script + Caption + Slides
└─────────────────────┘
```

Three things that make it an **agent** and not a chatbot:
1. **Tool use** — calls a live external API, not just LLM knowledge
2. **Decision making** — autonomously picks which tool to call
3. **Multi-step state** — LangGraph passes shared memory across 4 nodes

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|---|---|---|
| LLM | Gemini 2.5 Flash | Fast, cheap, great at structured output |
| Orchestration | LangGraph | State machine for multi-step agent pipelines |
| Tool Protocol | MCP (Model Context Protocol) | Anthropic's open standard for AI tool use |
| Data Source | RapidAPI — Free football data | Agent built around 5 tested football MCP tool endpoints |
| Language | Python 3.10+ | - |
| Config | python-dotenv | Keep API keys out of code |

---

## 📊 Real Metrics

- ⏱️ Research time: **3–4 hours → under 60 seconds**
- 📦 Output per run: **3 titles + 3 hooks + 60s script + caption + 5 story slides**
- 🔧 Tools tested: multiple MCP football endpoints; 5 working endpoints are used by the agent
- 🚫 Zero hallucination: agent uses **only live fetched data**, not LLM memory

---

## 📁 Project Structure

```
ScoutAI/
│
├── analyst_v1.py       # Main agent — LangGraph pipeline
├── mcp_client.py       # Connects to RapidAPI via MCP protocol
├── config.py           # League name → verified ID mappings
├── tool_router.py      # Intent → tool name + args (the decision engine)
├── prompts.py          # All 3 LLM instructions (routing, analysis, content)
├── discover_tools.py   # Helper script for probing MCP tool endpoints
├── find_league_ids.py  # Helper script for discovering league IDs
├── test_mcp.py         # MCP tool sanity checks
├── test_mcp_connection.py # MCP connection test
├── mcp.json            # MCP server config (RapidAPI connection)
├── .env                # API keys (never commit this)
├── .gitignore
```

---

## ⚡ Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/Aryanmehta11/AI-Sports-Agent-ScoutAI.git
cd AI-Sports-Agent-ScoutAI
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install langgraph langchain-google-genai python-dotenv mcp
```

### 4. Set up your `.env` file
```bash
# Create .env in the root folder
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Set up your `mcp.json` file
```json
{
  "mcpServers": {
    "RapidAPI Football": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: free-api-live-football-data.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY_HERE"
      ]
    }
  }
}
```

### 6. Run the agent
```bash
python analyst_v1.py
```

---

## 💬 Questions That Work

```
"What are the biggest transfers right now?"
"Give me the latest Premier League news"
"What's trending in football today?"
"Give me Champions League news"
"Any football news today?"
```

---

## 📤 Output Example

For the question *"What are the biggest transfers right now?"* you get:

```
🎬 YOUTUBE SHORTS
─────────────────
📌 3 TITLES
1. This Transfer Will BREAK The Internet 🤯
2. Nobody Saw This Signing Coming...
3. £80M Deal CONFIRMED — Football Is Wild

📌 3 HOOKS
1. "Nobody is talking about this transfer but it changes everything..."
2. "I can't believe this club just spent £80M on him..."
3. "Be honest — did you see this signing coming?"

📌 60-SECOND SCRIPT
[0-3s]   HOOK: Nobody is talking about this...
[3-15s]  CONTEXT: Here's what just happened...
[15-45s] THE MEAT: 3 jaw-dropping facts...
[45-55s] HOT TAKE: Here's my opinion...
[55-60s] CTA: Drop your thoughts below 👇

📸 INSTAGRAM
────────────
📌 REEL HOOK: "£80M. One player. Is this genius or madness?"
📌 CAPTION + HASHTAGS
📌 5 STORY SLIDES
```

---

## 🧠 Key Engineering Decisions

**Multi-phase LLM use** — first call extracts structured JSON intent, second call analyzes the fetched data, and third call generates the final content. Separating these stages makes it easier to swap or tune each phase independently.

**MCP over direct REST** — building on the protocol Claude, Cursor, and the industry are standardising on. Future-proof by design.

**Honest fallback** — discovery showed that many endpoints fail on the free tier. Built automatic fallback logic so the agent always produces output regardless.

**Windows asyncio fix** — `WindowsProactorEventLoopPolicy` required for subprocess-based MCP on Windows. Documented here so you don't spend 2 hours debugging it.

---

## 🔜 What's Next

- [ ] Telegram bot — query from phone
- [ ] Web UI (FastAPI + React) — already built, coming soon
- [ ] Add more data sources (ESPN, Transfermarkt)
- [ ] True agentic loops — retry and self-correct on bad data

---

## 📹 Video Walkthrough

Full walkthrough video coming soon — live demo, architecture explained, real output generated on screen.

---

## 🤝 Contributing

PRs welcome. If you find an API endpoint that actually works on the free tier, open an issue — would love to expand the tool coverage.

---

## 📄 License

MIT — use it, build on it, ship it.

---

<p align="center">Built by <a href="https://github.com/Aryanmehta11">Aryan Mehta</a> | Building in public 🚀</p>
