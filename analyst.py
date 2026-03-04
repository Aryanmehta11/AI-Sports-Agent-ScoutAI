from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

def analyze_match(summary):

    system = SystemMessage(content="""
You are a cricket analyst.

Explain:

1. what happened
2. turning point
3. key player
""")

    response = llm.invoke([
        system,
        HumanMessage(content=summary)
    ])

    return response.content