from langgraph.graph import StateGraph, END

from agent.state import PricingAgentState

from agent.nodes.intent_node import intent_node
from agent.nodes.retrieval_node import retrieval_node
from agent.nodes.confidence_node import confidence_node
from agent.nodes.escalation_node import escalation_node
from agent.nodes.answer_node import answer_node


builder = StateGraph(PricingAgentState)

builder.add_node("intent", intent_node)
builder.add_node("retrieval", retrieval_node)
builder.add_node("confidence", confidence_node)
builder.add_node("escalation", escalation_node)
builder.add_node("answer", answer_node)


builder.set_entry_point("intent")

builder.add_edge("intent", "retrieval")
builder.add_edge("retrieval", "confidence")
builder.add_edge("confidence", "escalation")
builder.add_edge("escalation", "answer")
builder.add_edge("answer", END)

graph = builder.compile()
