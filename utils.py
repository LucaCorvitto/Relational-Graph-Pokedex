from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import yaml
import os
import re
import time
from neo4j import GraphDatabase
from neo4j.exceptions import SessionExpired, ServiceUnavailable, TransientError
import logging
import csv
from my_langgraph_definition import building_pokemon_graph

DEBUG = True
API=False
GEN_MODEL="llama3.1:8b"
CODE_MODEL="qwen2.5-coder:7b"

# use this to create an instance of all the pokemon names in the dataset to be used in other functions
def extract_pokemon_names(csv_file_path):
    pokemon_names = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get("name")
            if name:
                pokemon_names.append(name.strip())
    return pokemon_names

# --- Setup logging ---
logging.basicConfig(
    filename="requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def initialization(debug=False, api=False, gen_model="gemma3:1b", code_model="gemma3:1b"):
    if debug:
    # SECRETS
        with open("secrets.yaml","r") as s:
            secrets = yaml.safe_load(s)

        OPENAI_API_KEY = secrets["OPENAI_API_KEY"]
        PINECONE_API_KEY = secrets["PINECONE_API_KEY"]
        INDEX_NAME = secrets["INDEX_NAME"]
        NEO4J_URI = secrets["NEO4J_URI"]
        NEO4J_AUTH = (secrets["NEO4J_USER"], secrets["NEO4J_PASSWORD"])
        NEO4J_DB = secrets["DATABASE"]

    else:
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        INDEX_NAME = os.getenv("INDEX_NAME")
        NEO4J_URI = os.getenv("NEO4J_URI")
        NEO4J_AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        NEO4J_DB = os.getenv("DATABASE")

    if api:
        embed_model = OpenAIEmbeddings(model="text-embedding-3-small", api_key= OPENAI_API_KEY)
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)
        code_llm = llm
    else:
        embed_model = OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11435")
        llm = ChatOllama(model=gen_model, temperature=0, base_url="http://127.0.0.1:11435") #
        code_llm = ChatOllama(
            model=code_model,
            temperature=0,
            base_url="http://127.0.0.1:11435")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    spec = ServerlessSpec(cloud="aws", region="us-east-1")

    if INDEX_NAME not in [idx["name"] for idx in pc.list_indexes()]:
        pc.create_index(INDEX_NAME, dimension=1536, metric="cosine", spec=spec)
        while not pc.describe_index(INDEX_NAME).status["ready"]:
            time.sleep(1)
    index = pc.Index(INDEX_NAME)

    vectorstore = PineconeVectorStore(index=index, embedding=embed_model)
    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

    pokemon_names_list = extract_pokemon_names('data/pokemon_data.csv')

    return {"llm":llm,
            "code_llm":code_llm,
            "vectorstore":vectorstore,
            "driver":driver,
            "secrets":
                {
                "NEO4J_URI":NEO4J_URI,
                "NEO4J_AUTH":NEO4J_AUTH,
                "NEO4J_DB":NEO4J_DB
                },
            "pokemon_names":pokemon_names_list
            }

def build_graph(debug=DEBUG, api=API, gen_model=GEN_MODEL, code_model=CODE_MODEL):
    # --- Init ---
    init = initialization(debug, api, gen_model, code_model)
    llm = init["llm"]
    code_llm = init["code_llm"]
    vectorstore = init["vectorstore"]
    driver = init["driver"]
    NEO4J_URI = init["secrets"]["NEO4J_URI"]
    NEO4J_AUTH = init["secrets"]["NEO4J_AUTH"]
    pokemon_names = init["pokemon_names"]

    pokemon_graph_agent = building_pokemon_graph(llm, code_llm, vectorstore, driver, NEO4J_URI, NEO4J_AUTH)

    return pokemon_graph_agent, pokemon_names, driver

# def extract_cypher_query(text: str) -> str:
#     """
#     Extracts and returns a cleaned Cypher query string from:
#     - Markdown-style code block ```cypher ... ```
#     - Free text that contains a Cypher query with known keywords

#     Returns an empty string if no query is found.
#     """

#     # First, try to extract from markdown code block
#     markdown_match = re.search(r"```cypher\s+(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
#     if markdown_match:
#         code_block = markdown_match.group(1)
#         return " ".join(line.strip() for line in code_block.strip().splitlines())

#     # Otherwise, look for free-form Cypher queries in the text
#     cypher_keywords = r"(MATCH|CREATE|MERGE|RETURN|DELETE|DETACH|SET|WITH|UNWIND|OPTIONAL\s+MATCH)"
#     pattern = re.compile(rf"\b(?:{cypher_keywords})\b.*?(?:;|\n|$)", re.IGNORECASE | re.DOTALL)
#     match = pattern.search(text)

#     if match:
#         query = match.group(0)
#         return " ".join(line.strip() for line in query.strip().splitlines())

#     return ""  # No valid Cypher query found



def extract_graph_from_neo4j(result):
    nodes = {}
    edges = []

    for record in result:
        path = record["path"]

        # Estrai tutti i nodi del cammino
        for node in path.nodes:
            node_id = node.id
            if node_id not in nodes:
                nodes[node_id] = {
                    "id": node_id,
                    "label": node.get("name", "unknown"),
                    "group": list(node.labels)[0] if node.labels else "Unknown"
                }

        # Estrai tutte le relazioni (archi) del cammino
        for rel in path.relationships:
            edges.append({
                "from": rel.start_node.id,
                "to": rel.end_node.id,
                "label": rel.type
            })

    return list(nodes.values()), edges


# def get_type_graph(driver, graph_info, max_retries=3):
#     # Estraggo nomi tipi
#     list_of_types = [elem["t.name"] for elem in graph_info if "t.name" in elem]

#     if not list_of_types:
#         return [], []

#     for attempt in range(max_retries):
#         try:
#             with driver.session() as session:
#                 cypher = """
#                 MATCH (t:Type)
#                 WHERE t.name IN $names
#                 WITH collect(t) AS ts
#                 UNWIND ts AS t1
#                 UNWIND ts AS t2
#                 WITH t1, t2 WHERE elementId(t1) < elementId(t2)
#                 MATCH path = allShortestPaths((t1)-[*..2]-(t2))
#                 RETURN path
#                 """
#                 result = session.run(cypher, parameters={"names": list_of_types})
#                 nodes, edges = extract_graph_from_neo4j(result)
#                 return nodes, edges
#         except (SessionExpired, ServiceUnavailable, TransientError) as e:
#             print(f"Neo4j connection error: {e}. Retrying ({attempt+1}/{max_retries})...")
#             time.sleep(1 * (attempt+1))
#     return [], []


def get_pokemon_relational_graph(driver, list_of_nodes, max_retries=3):
    #list_of_nodes = [elem["p.name"] for elem in graph_info]

    for attempt in range(max_retries):
        try:
            with driver.session() as session:
                cypher = """
                MATCH (p:Pokemon)
                WHERE p.name IN $names
                WITH collect(p) AS ps
                UNWIND ps AS p1
                UNWIND ps AS p2
                WITH p1, p2 WHERE elementId(p1) < elementId(p2)
                MATCH path = allShortestPaths((p1)-[*..2]-(p2))
                RETURN path
                """
                result = session.run(cypher, parameters={"names": list_of_nodes})
                nodes, edges = extract_graph_from_neo4j(result)
                return nodes, edges
        except (SessionExpired, ServiceUnavailable, TransientError) as e:
            print(f"Neo4j connection error: {e}. Retrying ({attempt+1}/{max_retries})...")
            time.sleep(1 * (attempt+1))
    raise Exception("Max retries exceeded")

def get_graph_by_type(driver, graph_info, pokemon_names):
    # if any("p.name" in elem for elem in graph_info):
    #     return get_pokemon_relational_graph(driver, graph_info)
    # elif any("t.name" in elem for elem in graph_info):
    #     return get_type_graph(driver, graph_info)
    # qui puoi aggiungere altri casi (categorie, ecc)
    list_of_nodes = []
    for dict in graph_info: # iterate over all the dictionary in graph_info
        logging.info(f"dictionary in graph info: {dict}")
        for key,value in dict.items(): # iterate over keys and values (just to extract the first key, value pair)
            if value in pokemon_names:
                list_of_nodes = [elem[key] for elem in graph_info]
            break
    # what to do if graph_info does not contain any pokemon name?
    if list_of_nodes:
        return get_pokemon_relational_graph(driver, list_of_nodes)
    # Nessun nodo grafico riconosciuto → ritorno vuoto
    else:
        return [], []

def run_pokemon_query(query, pokemon_graph_agent, pokemon_names, driver):
    #pokemon_graph_agent, pokemon_names, driver = build_graph()
    logging.info(f"Received query: {query}")

    initial_input = {"query": query}
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

        nodes, edges = get_graph_by_type(driver, graph_info, pokemon_names)
        print("nodes:", nodes)
        print("edges:", edges)

        return {
            "response":response_text,
            "graph_info":graph_info,
            "nodes":nodes,
            "edges":edges
            }
    # QueryResponse(
    #         response=response_text,
    #         graph_info=graph_info,
    #         nodes=nodes,
    #         edges=edges
    #     )

    except Exception as e:
        logging.error(f"Error during processing query '{query}': {e}", exc_info=True)
        return {
            "response":"Errore interno del server",
            "graph_info":[],
            "nodes":[],
            "edges":[]
            }
        # return QueryResponse(
        #     response="Errore interno del server",
        #     graph_info=[],
        #     nodes=[],
        #     edges=[])