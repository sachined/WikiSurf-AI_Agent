from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool

# Reuse tool instances to avoid overhead and potential initialization issues
_ddg_search = DuckDuckGoSearchRun()
_wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
_wiki_search = WikipediaQueryRun(api_wrapper=_wiki_api_wrapper)

@tool
def search_tool(query: str) -> str:
    """Search the web for information using DuckDuckGo.
    
    Args:
        query: The search query string.
    """
    return _ddg_search.run(query)

def _clean_wikipedia_query(query: str) -> str:
    """Cleans a query by removing common wrapper characters or extra spaces."""
    return query.strip().replace('"', '').replace("'", "")

@tool
def wikipedia_tool(query: str) -> str:
    """Search Wikipedia for a specific topic.
    
    Provides a concise summary of the top result.
    
    Args:
        query: The topic to search for.
    """
    try:
        cleaned_query = _clean_wikipedia_query(query)
        return _wiki_search.run(cleaned_query)
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"
