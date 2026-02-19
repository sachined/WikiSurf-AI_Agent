from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from datetime import datetime

# Reuse tool instances to avoid overhead and potential initialization issues
_ddg_search = DuckDuckGoSearchRun()
_wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=1000)
_wiki_search = WikipediaQueryRun(api_wrapper=_wiki_api_wrapper)

@tool("save_text_to_file", description="Save structured research data to a text file.")
def save_to_txt(data: str, filename: str = "research_output.txt"):
    """Saves provided data to a text file with timestamped header.

    Args:
        data: The content to be saved.
        filename: The name of the file to save to. Defaults to 'research_output.txt'.

    Returns:
        A message indicating successful save.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, 'a', encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"

save_tool = save_to_txt

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
