from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from backend.services.agents.llm_provider import get_llm
from backend.services.agents.tools import get_tools


def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    llm = get_llm(provider, llm_id)
    tools = get_tools(allow_search)

    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    # Prepare the message history
    message_history = [SystemMessage(content=system_prompt)]
    
    # Convert the incoming messages to the proper format
    for msg in query:
        if isinstance(msg, dict):  # If messages come as dicts from API
            if msg["role"] == "user":
                message_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                message_history.append(AIMessage(content=msg["content"]))
        else:  # Fallback for other formats
            message_history.append(HumanMessage(content=msg))

    state = {
        "messages": message_history  # Note: key is "messages" not "message"
    }

    response = agent.invoke(state)
    ai_messages = [msg.content for msg in response.get("messages", []) 
                  if isinstance(msg, AIMessage)]
    
    return ai_messages[-1] if ai_messages else "No response from AI"