# main.py
# LangGraph chatbot with routing, memory (Postgres), and NATS-based dispatch.

import asyncio
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import HumanMessage
from config.config import DB_URI
from graph_router import create_router_graph
from dispatcher import dispatch_query_nats

async def main():
    print("🚀 LangGraph RAG system ready. Type 'q' to quit.\n")

    # Init LangGraph w/ Postgres memory
    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
        checkpointer.setup()
        print("✅ Checkpointer initialized:", checkpointer)
        app = create_router_graph(checkpointer)

        while True:
            question = input("🧠 User Question: ").strip()
            if question.lower() == "q":
                break

            result = await app.ainvoke(
                {"messages": [HumanMessage(content=question)]},
                config={"configurable": {"session_id": "demo-user-1"}} 
            )
            
            response = result if isinstance(result, str) else str(result)

            print(f"\n🧾 Raw Final Response: {response}\n")

            # Try parsing the response as JSON
            try:
                import json
                parsed = json.loads(response)
                if "query_name" in parsed:
                    print(f"🔍 Routing Result: {parsed}")
                    final = await dispatch_query_nats(parsed)
                    print(f"✅ Final Answer: {final}\n")
                else:
                    print(f"🧠 Agent Message: {parsed.get('follow_up_question', response)}\n")
            except Exception as e:
                print(f"⚠️ Failed to parse final response: {e}")
                print(f"🧠 Agent Message: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())