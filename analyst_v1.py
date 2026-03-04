import json
import asyncio

from dotenv import load_dotenv
from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

from prompts import context_prompt, analysis_prompt, content_prompt
from mcp_client import call_mcp_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)


class AgentState(TypedDict):

    question: str
    context: dict
    data: dict
    analysis: str
    content: str


# -------- Context Extraction --------

def extract_context(state):

    question = state["question"]

    prompt = f"""
{context_prompt}

Question:
{question}
"""

    res = llm.invoke(prompt)

    try:
        context = json.loads(res.content)
    except:
        context = {}

    return {"context": context}


# -------- Fetch Match Data --------

def fetch_data(state):

    context = state["context"]

    # Example MCP tool
    data = asyncio.run(
        call_mcp_tool(
        "V3_-_Last_x_Fixtures_that_were_played",
        {
            "league": 140,   # La Liga
            "season": 2023,
            "last": 5
        }
    )
    )

    return {"data": data}


# -------- Match Analysis --------

def analyze_match(state):

    question = state["question"]
    data = state["data"]

    prompt = analysis_prompt.format(
        data=data,
        question=question
    )

    res = llm.invoke(prompt)

    return {"analysis": res.content}


# -------- Content Generator --------

def generate_content(state):

    analysis = state["analysis"]

    prompt = content_prompt.format(
        analysis=analysis
    )

    res = llm.invoke(prompt)

    return {"content": res.content}


# -------- Build Graph --------

builder = StateGraph(AgentState)

builder.add_node("context", extract_context)
builder.add_node("fetch", fetch_data)
builder.add_node("analysis", analyze_match)
builder.add_node("content", generate_content)

builder.set_entry_point("context")

builder.add_edge("context", "fetch")
builder.add_edge("fetch", "analysis")
builder.add_edge("analysis", "content")
builder.add_edge("content", END)

app = builder.compile()


# -------- Run Agent --------

if __name__ == "__main__":

    question = input("\nAsk a sports question: ")

    result = app.invoke({
        "question": question
    })

    print("\n===== MATCH ANALYSIS =====\n")
    print(result["analysis"])

    print("\n===== CREATOR CONTENT =====\n")
    print(result["content"])