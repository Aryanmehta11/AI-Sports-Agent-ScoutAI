from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

def extract_story(analysis):

    system = SystemMessage(content="""
You are a sports content strategist.

Find the biggest storyline.

Example:
"India collapsed under pressure"
"Pakistan pulled off miracle chase"
""")

    response = llm.invoke([
        system,
        HumanMessage(content=analysis)
    ])

    return response.content