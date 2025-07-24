from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field
from utils import *
from my_langgraph_definition import building_pokemon_graph
from Custom_log import init_log, log, DEBUG_log
import flet as ft

DEBUG=False
DEBUG=True            # decommenta per debug / commenta per produzione

# --- Setup logging ---
init_log(
    base_dir= "logs",
    print_debug= True if DEBUG else False,
    print_inputs= True if DEBUG else False
)

# --- Init ---
init = initialization(debug=DEBUG)
llm = init["llm"]
vectorstore = init["vectorstore"]
driver = init["driver"]
NEO4J_URI = init["secrets"]["NEO4J_URI"]
NEO4J_AUTH = init["secrets"]["NEO4J_AUTH"]

pokemon_graph_agent = building_pokemon_graph(llm, vectorstore, driver, NEO4J_URI, NEO4J_AUTH)

# --- Models ---
class Node(BaseModel):
    id: int
    label: str
    group: Optional[str] = None

class Edge(BaseModel):
    from_: int = Field(..., alias="from")
    to: int
    label: Optional[str] = None

class GraphResponse(BaseModel):
    response: str
    nodes: List[Node]
    edges: List[Edge]

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    graph_info: List[Dict[str, Union[str, int, float]]]
    nodes: List[Node]
    edges: List[Edge]

async def run_pokemon_query(request: QueryRequest):
    DEBUG_log(f"Received query: {request.query}")

    initial_input = {"query": request.query}
    thread = {"configurable": {"thread_id": "42"}}

    try:
        final_state = pokemon_graph_agent.invoke(initial_input, config=thread)
        response_text = final_state.get("response", "")
        graph_info = final_state.get("graph_info", [])

        DEBUG_log(f"Response: {response_text}")
        if graph_info:
            DEBUG_log(f"Graph info: {graph_info}")

        # Salva la graph_info per il GET
        #app.state.last_graph_info = graph_info

        nodes, edges = get_graph_by_type(driver, graph_info)
        print("nodes:", nodes)
        print("edges:", edges)

        return QueryResponse(
            response=response_text,
            graph_info=graph_info,
            nodes=nodes,
            edges=edges
        )

    except Exception as e:
        DEBUG_log(f"Error during processing query '{request.query}': {e}", level="ERROR")
        return QueryResponse(
            response="Errore interno del server",
            graph_info=[],
            nodes=[],
            edges=[])

def main(page: ft.Page):
    page.title = "Pokédex Graph"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Add your Flet UI components here
    page.add(ft.Text("Welcome to the Pokédex Graph!"))

# decommenta per debug / commenta per produzione
if __name__ == "__main__":
    ft.app(target=main)