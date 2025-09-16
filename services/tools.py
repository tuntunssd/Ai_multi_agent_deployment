from langchain_core.tools import tool
from langchain_tavily import TavilySearch
import os
from .model import llm

tavily_api_key = os.getenv("TAVILY_API_KEY")


def _format_results(results):
    """Helper to safely format Tavily results list."""
    if not results:
        return None

    formatted = []
    for r in results:
        if isinstance(r, dict):
            title = r.get("title", "Untitled")
            content = r.get("content", "")
            formatted.append(f"- {title}: {content[:200]}...")
        elif isinstance(r, str):
            formatted.append(f"- {r}")
    return "\n".join(formatted) if formatted else None


@tool
def news_search(query: str) -> str:
    """Search latest news about a topic."""
    try:
        search = TavilySearch(max_results=3, tavily_api_key=tavily_api_key)
        response = search.invoke(f"latest news about {query}")

        # Tavily returns a dict, so extract the `results` field
        results = response.get("results") if isinstance(response, dict) else response
        formatted = _format_results(results)
        return formatted or "No news found."
    except Exception as e:
        return f"News search error: {str(e)}"


@tool
def book_search(query: str) -> str:
    """Search for information about books."""
    try:
        search = TavilySearch(max_results=3, tavily_api_key=tavily_api_key)
        response = search.invoke(f"book information {query}")

        results = response.get("results") if isinstance(response, dict) else response
        formatted = _format_results(results)
        return formatted or "No books found."
    except Exception as e:
        return f"Book search error: {str(e)}"


@tool
def math_solver(expression: str) -> str:
    """Solve a math expression or problem."""
    try:
        if all(c in "0123456789.+-*/() " for c in expression):
            result = eval(expression, {"__builtins__": {}}, {})
            return str(result)

        prompt = f"Solve the following math problem and return only the final answer:\n\n{expression}"
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"Math error: {str(e)}"



