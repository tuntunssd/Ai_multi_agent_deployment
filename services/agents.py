from .tools import news_search, book_search, math_solver
from .model import llm
from langchain_core.runnables import RunnableLambda

# Each agent wraps its corresponding tool
news_agent = RunnableLambda(lambda state: {"answer": news_search(state["messages"][-1])})
math_agent = RunnableLambda(lambda state: {"answer": math_solver(state["messages"][-1])})
book_agent = RunnableLambda(lambda state: {"answer": book_search(state["messages"][-1])})

# Router agent: can be used as a placeholder if needed
def router_agent(state):
    return state

# Routing logic for 3 agents
def routing_logic(state):
    query = state["messages"][0]
    
    prompt = f"""
    You are a router agent. Choose the best agent for the query: {query}

    Available agents:
    - news_agent: Provides latest news.
    - math_agent: Solves math problems using the math_solver tool.
    - book_agent: Searches information about books.

    Respond with only the agent name: news_agent, math_agent, or book_agent.
    """
    
    try:
        response = llm.invoke(prompt)
        decision = response.content.strip().lower()
    except Exception:
        decision = query.lower()  # fallback if LLM fails
    
    # Basic keyword fallback routing
    if "news" in decision:
        return "news_agent"
    elif "book" in decision:
        return "book_agent"
    elif any(c in decision for c in "+-*/=") or "math" in decision:
        return "math_agent"
    else:
        # default to news_agent if no match
        return "news_agent"
