from langgraph.graph import StateGraph
from typing import TypedDict

from nodes.fetch_node import fetch_data
from nodes.calculate_node import calculate_salary
from nodes.pdf_node import generate_pdf

# Define state structure
class PayrollState(TypedDict):
    employee: dict
    salary: float
    pdf_path: str

# Build graph
builder = StateGraph(PayrollState)

builder.add_node("fetch", fetch_data)
builder.add_node("calculate", calculate_salary)
builder.add_node("pdf", generate_pdf)

builder.set_entry_point("fetch")

builder.add_edge("fetch", "calculate")
builder.add_edge("calculate", "pdf")

graph = builder.compile()