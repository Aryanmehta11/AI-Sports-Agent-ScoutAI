from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

def generate_content(story):

    system = SystemMessage(content="""
Create content for sports creators.

Return:

3 viral hooks
3 YouTube titles
Shorts script

Script structure:

HOOK
FACT
TWIST
ENGAGEMENT
""")

    response = llm.invoke([
        system,
        HumanMessage(content=story)
    ])

    return response.content