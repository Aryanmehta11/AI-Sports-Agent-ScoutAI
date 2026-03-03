import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch 
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

# 1. State Definition
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 2. Setup (Try 'gemini-1.5-flash' without the models/ prefix)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

search_tool = TavilySearch(max_results=3)
tools = [search_tool]
llm_with_tools = llm.bind_tools(tools)

# 3. Nodes
def call_model(state: AgentState):
    # We define the persona here
    system_message = SystemMessage(content="You are a professional sports analyst. Use the search tool to find facts.")
    messages = [system_message] + state['messages']
    
    # We call the model
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

# 4. Router
def should_continue(state: AgentState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 5. Graph Construction
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app = workflow.compile()

if __name__ == "__main__":
    # Simplified query for testing
    query = "Who won the last Real Madrid match?"
    inputs = {"messages": [HumanMessage(content=query)]}
    
    print("--- 🕵️ Starting Agent ---")
    try:
        for output in app.stream(inputs, stream_mode="updates"):
            for key, value in output.items():
                print(f"\n[Node: {key}]")
                if "messages" in value:
                    print(value["messages"][-1])
    except Exception as e:
        print(f"\n❌ Error Caught: {e}")