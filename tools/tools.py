from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name: str):
    """Seaches for linkedin or twitter Profile Page"""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res