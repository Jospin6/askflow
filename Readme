# AskFlow - Intelligent Internet-Connected Chatbot

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-ff6b35.svg)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.0+-7c3aed.svg)](https://langchain-ai.github.io/langgraph/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.24+-ff4b4b.svg)](https://streamlit.io/)
[![Tavily Search](https://img.shields.io/badge/Tavily-Search-7b68ee.svg)](https://tavily.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Render](https://img.shields.io/badge/API-Render-5fddc6.svg)](https://render.com/)
[![Streamlit Cloud](https://img.shields.io/badge/UI-Streamlit%20Cloud-ff4b4b.svg)](https://streamlit.io/cloud)

AskFlow is an intelligent chatbot application that leverages advanced AI decision-making to provide accurate responses by either answering directly from its knowledge or performing real-time internet searches using Tavily Search API.

## Features

- **Intelligent Decision Making**: LangGraph-powered agent that decides whether to answer directly or search the web
- **Real-time Internet Access**: Integrated Tavily Search API for up-to-date information
- **Conversational Memory**: Maintains context throughout conversations
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Modern Web Interface**: Streamlit-based responsive UI
- **Cloud Deployment**: Fully deployed and accessible online

## Live Demos

- **Web Interface**: [AskFlow Streamlit App](https://askflow.streamlit.app/)

## Tech Stack

- **AI Framework**: LangChain, LangGraph
- **Search API**: Tavily Search
- **Backend**: FastAPI, Uvicorn, Pydantic
- **Frontend**: Streamlit
- **LLM Integration**: OpenAI GPT (or your preferred LLM)
- **Deployment**: Render, Streamlit Cloud
- **Environment Management**: Poetry/Pipenv


## How It Works

### Decision Process Flow

1. **User Input**: User submits a question through the interface
2. **Agent Decision**: LangGraph agent analyzes whether to answer directly or search the web
3. **Execution**: Direct answer or web search via Tavily API
4. **Response Delivery**: Formatted response returned to user

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Tavily Search API key
- OpenAI API key (or alternative LLM provider)
- Poetry or Pipenv

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/askflow.git
cd askflow 
```

### Run the application locally
    ```bash
    # Start API server
    cd api && uvicorn main:app --reload

    # Start UI (in separate terminal)
    cd ui && streamlit run app.py
    ```