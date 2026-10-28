from langgraph.graph import END, START

from src.utils.edges import should_continue
from src.utils.nodes import create_analysts, dummy, human_feedback
from src.utils.states import GenerateAnalystsState, state_graph

# building our graph
builder = state_graph(GenerateAnalystsState)

builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback", human_feedback)
builder.add_node("dummy", dummy)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges(
    "human_feedback", should_continue, ["create_analysts", "dummy"]
)
builder.add_edge("dummy", END)

graph = builder.compile(interrupt_before=["human_feedback"])
