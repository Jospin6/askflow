from langchain_groq import ChatGroq
from backend.config import GROQ_API_KEY


def get_llm(provider, model):
    if provider == "Groq":
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY NOT FOUND")
        return ChatGroq(model=model, api_key=GROQ_API_KEY)
    else:
        raise ValueError(f"Unkwown provider: {provider}")