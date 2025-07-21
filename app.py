from langgraph.graph import StateGraph, add_messages, END
from typing import TypedDict, Annotated, Optional
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver
from uuid import uuid4
import json
load_dotenv()






