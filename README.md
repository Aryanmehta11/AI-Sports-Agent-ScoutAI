# ScoutAI: Agentic Sports Analyst ⚽🏏

ScoutAI is an autonomous research agent built to transform raw match data into high-engagement content for YouTube and Instagram creators. Unlike static chatbots, ScoutAI uses **agentic reasoning** to browse the live web, verify tactical stats, and synthesize production-ready insights.

## ✨ Features (Level 1)
- **Live Web Intelligence:** Integrated with Tavily AI for real-time search, bypassing LLM knowledge cut-offs.
- **Autonomous Reasoning:** Built on a cyclic **StateGraph** that allows the agent to self-correct and perform multi-turn research until a query is fully satisfied.
- **Context Preservation:** Maintains a persistent "Whiteboard" state to correlate findings across multiple search loops.

## 🛠️ Tech Stack
- **Orchestration:** LangGraph (Python)
- **Brain:** Gemini 2.5 Flash
- **Search Engine:** Tavily AI
- **Environment:** FastAPI & Dotenv

## 📦 Installation

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/yourusername/sports-analyst-agent.git](https://github.com/yourusername/sports-analyst-agent.git)
   cd sports-analyst-agent
