# graph_router.py

from langchain_core.runnables import RunnableLambda
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap
from langgraph.graph import END, START, StateGraph
from langchain_core.runnables.history import RunnableWithMessageHistory
from query_bank import QUERY_BANK
from llm.ollama_llm import get_llm
from config.config import DB_URI

# Build the system prompt from the query bank
def build_router_prompt():
    query_descriptions = "\n".join(
        [f"- {q['name']}: {q['description']} (params: {', '.join(q['params'])})" for q in QUERY_BANK]
    )
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are a routing agent in a logistics RAG system.\n"
                    "Your job is to decide which predefined query best matches the user's request.\n"
                    f"Available queries:\n{query_descriptions}\n\n"
                    "User question: {question}\n\n"
                    "If all required parameters are present, respond ONLY with a compact JSON like:\n"
                    '{{"query_name": "...", "plate": "...", "start_date": "...", "end_date": "..."}}\n\n'
                    "If missing info, respond with:\n"
                    '{{"follow_up_question": "What info is missing and what should the user provide?"}}'
                )
            )
        ]
    )

def create_router_graph(checkpointer):
    prompt = build_router_prompt()
    llm = get_llm()
    print("📦 Checkpointer passed to RunnableWithMessageHistory:", checkpointer)

    def route_fn(state):
        messages = state.get("messages", [])
        question = messages[-1].content if messages else ""
        return {"messages": prompt.format_messages(question=question)}

    router_node = RunnableLambda(route_fn) | RunnableLambda(lambda d: d["messages"]) | llm

    # Create and compile the graph
    graph = (
        StateGraph(state_schema=dict)
        .add_node("router", router_node)
        .add_edge(START, "router")
        .add_edge("router", END)
    ).compile()
    
    def extract_session_id(config):
        if isinstance(config, dict):
            return config.get("configurable", {}).get("session_id", "default-session")
        return "default-session"

    return RunnableWithMessageHistory(
        runnable=graph,
        get_session_history=lambda session_id: PostgresChatMessageHistory(
            session_id=session_id,
            connection_string=DB_URI
        ),
        get_session_id=extract_session_id,
        input_messages_key="messages",
        history_messages_key="messages",
    )



    
