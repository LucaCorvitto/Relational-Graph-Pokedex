from fastapi import FastAPI
from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import logging
from utils import *
from my_langgraph_definition import building_pokemon_graph
from fastapi.staticfiles import StaticFiles
import uvicorn

DEBUG=False
DEBUG=True            # decommenta per debug / commenta per produzione
GEN_MODEL="mistral:7b"
CODE_MODEL="qwen2.5-coder:7b"

# --- Setup logging ---
logging.basicConfig(
    filename="requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Init ---
init = initialization(debug=DEBUG)
llm = init["llm"]
code_llm = init["code_llm"]
vectorstore = init["vectorstore"]
driver = init["driver"]
NEO4J_URI = init["secrets"]["NEO4J_URI"]
NEO4J_AUTH = init["secrets"]["NEO4J_AUTH"]

pokemon_graph_agent = building_pokemon_graph(llm, code_llm, vectorstore, driver, NEO4J_URI, NEO4J_AUTH)

app = FastAPI(title="Pokémon LangGraph API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/query", response_model=QueryResponse)
async def run_pokemon_query(request: QueryRequest):
    logging.info(f"Received query: {request.query}")

    initial_input = {"query": request.query}
    thread = {"configurable": {"thread_id": "42"}}

    try:
        final_state = pokemon_graph_agent.invoke(initial_input, config=thread)
        response_text = final_state.get("response", "")
        graph_info = final_state.get("graph_info", [])

        logging.info(f"Response: {response_text}")
        if graph_info:
            logging.info(f"Graph info: {graph_info}")

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
        logging.error(f"Error during processing query '{request.query}': {e}", exc_info=True)
        return QueryResponse(
            response="Errore interno del server",
            graph_info=[],
            nodes=[],
            edges=[])

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# decommenta per debug / commenta per produzione
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
