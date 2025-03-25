# Old LangChain agent setup for autonomous tool execution.
# Automatically builds and executes SQL queries based on user questions.
# Replaced by the router-dispatcher system, but can be reused for multi-tool agent workflows.

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from llm.ollama_llm import get_llm
from tools.sql_tool import get_sql_tool
from config.config import OLLAMA_MODEL

llm = get_llm(OLLAMA_MODEL)

sql_tool = get_sql_tool()

tools = [
    Tool(
        name="QueryDB",
        func=sql_tool,
        description=(
            "Use this tool to execute raw SQL SELECT queries on the database. "
            "Only use it for data retrieval — like counting rows, filtering records, or listing entries. "
            "Always write valid SQL. Return the result as plain English."
        )
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True 
)

def run_agent(user_query: str) -> str:
    return agent.invoke({"input": user_query})