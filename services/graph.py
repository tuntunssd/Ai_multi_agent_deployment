from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated
from .agents import news_agent, math_agent, book_agent, router_agent, routing_logic

# Define state structure
class State(TypedDict):
    messages: Annotated[list, "add_messages"]
    answer: str

def build_graph():
    graph = StateGraph(State)

    # Add all nodes
    graph.add_node("router_agent", router_agent)  # decides which agent to use
    graph.add_node("news_agent", news_agent)
    graph.add_node("math_agent", math_agent)
    graph.add_node("book_agent", book_agent)

    # START -> router_agent
    graph.add_edge(START, "router_agent")

    # router_agent chooses one of the three agents based on routing_logic
    graph.add_conditional_edges("router_agent", routing_logic, {
        "news_agent": "news_agent",
        "math_agent": "math_agent",
        "book_agent": "book_agent"
    })

    # All agents go to END
    graph.add_edge("news_agent", END)
    graph.add_edge("math_agent", END)
    graph.add_edge("book_agent", END)

    return graph.compile()


