from langchain_tavily import TavilySearch


def get_tools(enable: bool):
    return [TavilySearch(max_results=2)] if enable else []