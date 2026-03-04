import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict

load_dotenv()

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)

# Search Tool
search_tool = TavilySearch(max_results=5)

# State
class AgentState(TypedDict):
    question: str
    research: str
    analysis: str
    content: str


# -----------------------------
# NODE 1 — Research
# -----------------------------
def research_node(state):

    question = state["question"]

    results = search_tool.invoke(question)

    return {"research": str(results)}


# -----------------------------
# NODE 2 — Match Analyst
# -----------------------------
def analysis_node(state):

    prompt = f"""
You are a professional cricket and football analyst.

Based on this research:

{state['research']}

Answer the question:
{state['question']}

Explain:

1. match summary
2. why the team lost
3. turning point
4. key player
"""

    response = llm.invoke(prompt)

    return {"analysis": response.content}


# -----------------------------
# NODE 3 — Content Generator
# -----------------------------
def content_node(state):

    prompt = f"""
You are a YouTube sports creator assistant.

Based on this analysis:

{state['analysis']}

Generate:

3 viral hooks
3 YouTube titles
Shorts script

Script format:

HOOK
FACT
TWIST
ENGAGEMENT
"""

    response = llm.invoke(prompt)

    return {"content": response.content}


# -----------------------------
# BUILD GRAPH
# -----------------------------
builder = StateGraph(AgentState)

builder.add_node("research", research_node)
builder.add_node("analysis", analysis_node)
builder.add_node("content", content_node)

builder.set_entry_point("research")

builder.add_edge("research", "analysis")
builder.add_edge("analysis", "content")
builder.add_edge("content", END)

app = builder.compile()


# -----------------------------
# RUN AGENT
# -----------------------------
if __name__ == "__main__":

    question = input("\nAsk a sports question: ")

    result = app.invoke({
        "question": question
    })

    print("\n===== MATCH ANALYSIS =====\n")
    print(result["analysis"])

    print("\n===== CREATOR CONTENT =====\n")
    print(result["content"])