from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from web_api import web_search
from coder import coder
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

@tool
def web_api(query: str):
    """
    Searches the web for dynamic and updating information and code documentation.
    Extracts information from any links presnt in query.
    """
    return web_search(query)

@tool
def code_helper(query, chat=[],history=[]):
    """
    Write, Execute or Explain code.
    """
    return coder(query,chat,history)

# prompt = """
# ====================================================SYSTEM MESSAGE====================================================
# You are a Professional Software Developer Agent. Your Job is to answer all the users query as correctly as possible.
# You should always search the web for relevant documentation and examples before writing any code.
# =====================================================CHAT HISTORY=====================================================
# {chat history}
# =====================================================USER MESSAGE=====================================================
# {input}
# ==================================================MESSAGE PLACEHOLDER==================================================
# {agent_scratchpad}
# """

prompt = hub.pull("shankerabhigyan/openai-tools-agent-darwin")
# read prompt.txt

if __name__ == "__main__":
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    
    tools = [web_api, code_helper]

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True)
    agent_executor.invoke(
        {
            "input" : "write python code implemeting a binary search tree",
        }
    )