import asyncio
from dispatcher import dispatch_query_nats
from router_agent import route_user_question

async def main():
    print("🚀 RAG system ready. Type 'q' to quit.\n")

    while True:
        question = input("🧠 User Question: ").strip()
        if question.lower() == "q":
            break

        routing_result = route_user_question(question)

        # Follow-up loop
        while "follow_up_question" in routing_result:
            print(f"❓ Follow-up: {routing_result['follow_up_question']}")
            user_response = input("🧠 User Answer: ").strip()
            routing_result = route_user_question(user_response)

        if "query_name" not in routing_result:
            print("❌ No query selected by the agent.\n")
            continue

        print(f"🔍 Routing Result: {routing_result}")

        final_response = await dispatch_query_nats(routing_result)
        print(f"✅ Final Answer: {final_response}\n")

if __name__ == "__main__":
    asyncio.run(main())
