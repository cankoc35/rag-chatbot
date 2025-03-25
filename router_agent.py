from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
from query_bank import QUERY_BANK
from config.config import OLLAMA_MODEL
import json
import re 

query_descriptions = "\n".join(
    [f"- {q['name']}: {q['description']} (params: {', '.join(q['params'])})" for q in QUERY_BANK]
)

prompt = PromptTemplate(
    template=(
        "You are a routing agent in a logistics RAG system.\n"
        "Your job is to decide which predefined query best matches the user's request.\n"
        "Available queries:\n"
        f"{query_descriptions}\n\n"
        "User question: {question}\n\n"
        "If all required parameters for a query are available in the question, "
        "respond ONLY with a compact JSON like this:\n"
        '{{"query_name": "...", "plate": "...", "start_date": "...", "end_date": "..."}}\n\n'
        "If some parameters are missing, respond with:\n"
        '{{"follow_up_question": "What info is missing and what should the user provide?"}}'
    ),
    input_variables=["question"]
)

llm = Ollama(model=OLLAMA_MODEL)
router_chain = LLMChain(llm=llm, prompt=prompt)

def route_user_question(question: str) -> dict:
    output = router_chain.run({"question": question})
    
    print("\n🧾 Raw LLM Output ↓↓↓")
    print(output)

    # Try to extract JSON substring from the full output
    try:
        json_str = re.search(r'\{.*\}', output, re.DOTALL).group()
        parsed = json.loads(json_str)
    except Exception as e:
        print(f"❌ Failed to extract/parse JSON: {e}")
        return {}

    if "query_name" not in parsed:
        follow_up = parsed.get("follow_up_question", "Sorry, I need more info.")

        if "query_name" in follow_up:
            print("🛑 Model leaked internal info. Rephrasing...")
            follow_up = "Can you provide the missing information, like plate number or shipment ID?"

        return {"follow_up_question": follow_up}

    return parsed

