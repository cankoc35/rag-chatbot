from langchain_community.llms import Ollama
from config.config import OLLAMA_MODEL

def get_llm(model_name: str = OLLAMA_MODEL):
    """
    Returns an LLM instance configured to use an Ollama model.
    """
    return Ollama(model=model_name)