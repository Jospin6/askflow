from langgraph.graph import StateGraph, add_messages, END
from typing import TypedDict, Annotated, Optional
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from uuid import uuid4
from langgraph.prebuilt import ToolNode
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
load_dotenv()

model = ChatGroq(model="llama3-70b-8192")
search_tool = TavilySearch(max_results=4)

tools = [search_tool]

memory = MemorySaver()

llm_with_tools = model.bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list, add_messages]

async def model_node(state: State) -> State:
    """
    Process the messages and return the state with updated messages.
    """

    # Process the human message using the LLM with tools
    response = await llm_with_tools.ainvoke(
        state['messages'],)
    
    return {
        "messages": [response]
    }

async def tool_router(state: State) -> State:
    """
    Route the tool calls to the appropriate tool.
    """
    # Extract the last message
    last_message = state['messages'][-1]

    if (hasattr(last_message, 'tool_calls') and
            len(last_message.tool_calls) > 0):
        return "tool_node"
    else:
        return END

tool_node = ToolNode(tools=tools)

graph_builder = StateGraph(State)

graph_builder.add_node("model", model_node)
graph_builder.add_node("tool_node", tool_node)
graph_builder.add_node("tool_router", tool_router)  # ✅ ajout manquant ici

graph_builder.set_entry_point("model")

graph_builder.add_conditional_edges("model", tool_router)
graph_builder.add_edge("tool_router", "model")

graph = graph_builder.compile(checkpointer=memory)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type"],
)

# async def generate_chat_response(message: str, checkpoint_id: Optional[str] = None):
#     is_new_conversation = checkpoint_id is None

#     if is_new_conversation:
#         new_checkpoint_id = str(uuid4()) 

#         config = {
#             "configurable": {
#                 "thread_id": new_checkpoint_id
#             }
#         }

#         events = graph.astream_events(
#             {"messages": [HumanMessage(content=message)]},
#             config=config,
#         )

#         yield f"data: {{\"type\": \"checkpoint\", \"checkpoint_id\": \"{new_checkpoint_id}\"}}\n\n"
#     else:
#         config = {
#             "configurable": {
#                 "thread_id": checkpoint_id
#             }
#         }

#         events = graph.astream_events(
#             {"messages": [HumanMessage(content=message)]},
#             config=config,
#         )

#     async for event in events:
#         event_type = event["event"]

#         if event_type == "on_chat_model_stream":
#             chunk_content = serialise_ai_message(event["data"]["chunk"])
#             safe_content = chunk_content.replace("'", "\\").replace("\n", "\\n")
#             yield f"data: {{\"type\": \"content\", \"content\": \"{safe_content}\"}}\n\n"

#         elif event_type == "on_tool_end":
#             tool_message = event["data"]["output"].tool_calls if hasattr(event["data"]["output"], "tool_calls") else []
#             search_calls = [call for call in tool_message if call["name"] == "tavily_search"]
#             if search_calls:
#                 search_results = search_calls[0].get("result", {}).get("results", [])
#                 if search_results:
#                     results_content = "\n".join([f"{result['title']}: {result['url']}" for result in search_results])
#                     yield f"data: {{\"type\": \"search_results\", \"content\": \"{results_content}\"}}\n\n"



# @app.get("/chat_stream/{message}")
# async def chat_stream(
#     message: str, 
#     checkpoint_id: Optional[str] = Query(None)
# ):
#     """
#     Stream chat responses based on the input message.
#     """
#     return StreamingResponse(
#         generate_chat_response(message, checkpoint_id),
#         media_type="text/event-stream")

    
thread_id = str(uuid4())

config = {
    "configurable": {
        "thread_id": thread_id
    }
}

async def main():
    async for event in graph.astream({
        "messages": [
            HumanMessage(content="c'est quoi l'actuallité en afrique aujourd'hui ?")
        ]
    }, config=config):
        if isinstance(event, dict):
            for node_name, node_data in event.items():
                if isinstance(node_data, dict):
                    messages = node_data.get("messages", [])
                    for message in messages:
                        if hasattr(message, "content") and message.content:
                            print(message.content, end="", flush=True)

asyncio.run(main())
