import os
from typing import Any, Dict, List, TypedDict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# ---------------------
# Modèle LLM
# ---------------------
llm = ChatGroq(model="llama3-70b-8192", temperature=0, api_key=groq_api_key)

# ---------------------
# Outils
# ---------------------
# wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
serp_tool = TavilySearch(
    max_results=3,            # Nombre max de résultats
    include_images=True,      # Inclure les images
    include_answer=True,      # Inclure un résumé
    include_raw_content=True,
)

# ---------------------
# État partagé
# ---------------------
class MultiAgentState(TypedDict):
    query: str
    info: List[Dict[str, Any]]
    draft: str
    quality: str
    images: List[str]
    sources: List[str]

# ---------------------
# Noeud Décisionnaire
# ---------------------
def decision_maker(state: MultiAgentState) -> MultiAgentState:
    """Décide s'il faut chercher des infos ou répondre directement"""
    decision_prompt = f"""
    Question: {state['query']}
    Dois-je chercher plus d'infos avant de répondre ?
    Réponds par 'oui' ou 'non'.
    """
    decision = llm.invoke(decision_prompt).content.strip().lower()
    state["decision"] = decision
    return state

# ---------------------
# Agents
# ---------------------
def recherche(state: MultiAgentState) -> MultiAgentState:
    print("🔍 Recherche d'informations...")
    serp_res = serp_tool.invoke(state["query"])  # dict avec results, images, answer...
    
    # Stocke la liste complète des résultats
    state["info"] = serp_res.get("results", [])
    
    # Récupère les images globales (liste)
    state["images"] = serp_res.get("images", [])
    
    # Récupère les sources depuis chaque résultat
    state["sources"] = [item.get("url") for item in serp_res.get("results", []) if "url" in item]
    
    return state

# ---------------------
# Noeud Rédaction + Amélioration
# ---------------------
def redacteur(state: MultiAgentState) -> MultiAgentState:
    print("✍️ Rédaction de la réponse...")
    infos_text = "\n".join([item.get("content", "") for item in state.get("info", [])])
    prompt = f"""
    Question: {state['query']}
    Infos trouvées : {infos_text}
    Écris une réponse claire et complète en français.
    """
    draft = llm.invoke(prompt).content
    state["draft"] = draft

    # Évaluation de la qualité
    quality_prompt = f"""
    Réponse : {draft}
    Est-ce que cette réponse est claire, complète et précise ?
    Réponds par 'bonne' ou 'mauvaise'.
    """
    quality = llm.invoke(quality_prompt).content.strip().lower()
    state["quality"] = quality

    # Si mauvaise, amélioration
    if quality == "mauvaise":
        improve_prompt = f"""
        Réponse actuelle : {draft}
        Améliore cette réponse en ajoutant des détails précis et pertinents.
        """
        state["draft"] = llm.invoke(improve_prompt).content

    return state

# ---------------------
# Construction du graphe LangGraph
# ---------------------
graph = StateGraph(MultiAgentState)

graph.add_node("decision", decision_maker)
graph.add_node("recherche", recherche)
graph.add_node("redaction", redacteur)

# Logique conditionnelle
graph.add_conditional_edges(
    "decision",
    lambda state: "recherche" if state["decision"] == "oui" else "redaction",
    {"recherche": "redaction", "redaction": "redaction"}
)

graph.add_edge("redaction", END)

graph.set_entry_point("decision")
workflow = graph.compile()

# ---------------------
# API FastAPI
# ---------------------
app = FastAPI(title="Multi-Agents API")

class QueryRequest(BaseModel):
    query: str

@app.post("/run")
async def run_multi_agents(request: QueryRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="La requête ne peut pas être vide")
    
    try:
        result = workflow.invoke(MultiAgentState(query=query))
        return {
            "query": query,
            "result": result["draft"],
            "sources": result.get("sources", []),
            "images": result.get("images", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")
# ---------------------
# Lancement du serveur
# ---------------------
# uvicorn main:app --reload
