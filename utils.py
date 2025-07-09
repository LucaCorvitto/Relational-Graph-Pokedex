from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import yaml
import os
import time
from neo4j import GraphDatabase
from neo4j.exceptions import SessionExpired, ServiceUnavailable, TransientError

def initialization():
    # SECRETS
    # with open("secrets.yaml","r") as s:
    #     secrets = yaml.safe_load(s)

    # OPENAI_API_KEY = secrets["OPENAI_API_KEY"]
    # PINECONE_API_KEY = secrets["PINECONE_API_KEY"]
    # INDEX_NAME = secrets["INDEX_NAME"]
    # NEO4J_URI = secrets["NEO4J_URI"]
    # NEO4J_AUTH = (secrets["NEO4J_USER"], secrets["NEO4J_PASSWORD"])
    # NEO4J_DB = secrets["DATABASE"]

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    INDEX_NAME = os.getenv("INDEX_NAME")
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
    NEO4J_DB = os.getenv("DATABASE")

    embed_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
    pc = Pinecone(api_key=PINECONE_API_KEY)
    spec = ServerlessSpec(cloud="aws", region="us-east-1")

    if INDEX_NAME not in [idx["name"] for idx in pc.list_indexes()]:
        pc.create_index(INDEX_NAME, dimension=1536, metric="cosine", spec=spec)
        while not pc.describe_index(INDEX_NAME).status["ready"]:
            time.sleep(1)
    index = pc.Index(INDEX_NAME)
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    vectorstore = PineconeVectorStore(index=index, embedding=embed_model)
    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

    return {"llm":llm,
            "vectorstore":vectorstore,
            "driver":driver,
            "secrets":
                {
                "NEO4J_URI":NEO4J_URI,
                "NEO4J_AUTH":NEO4J_AUTH,
                "NEO4J_DB":NEO4J_DB
                }
            }

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


def get_type_graph(driver, graph_info, max_retries=3):
    # Estraggo nomi tipi
    list_of_types = [elem["t.name"] for elem in graph_info if "t.name" in elem]

    if not list_of_types:
        return [], []

    for attempt in range(max_retries):
        try:
            with driver.session() as session:
                cypher = """
                MATCH (t:Type)
                WHERE t.name IN $names
                WITH collect(t) AS ts
                UNWIND ts AS t1
                UNWIND ts AS t2
                WITH t1, t2 WHERE elementId(t1) < elementId(t2)
                MATCH path = allShortestPaths((t1)-[*..2]-(t2))
                RETURN path
                """
                result = session.run(cypher, parameters={"names": list_of_types})
                nodes, edges = extract_graph_from_neo4j(result)
                return nodes, edges
        except (SessionExpired, ServiceUnavailable, TransientError) as e:
            print(f"Neo4j connection error: {e}. Retrying ({attempt+1}/{max_retries})...")
            time.sleep(1 * (attempt+1))
    return [], []



def get_pokemon_relational_graph(driver, graph_info, max_retries=3):
    list_of_nodes = [elem["p.name"] for elem in graph_info]

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

def get_graph_by_type(driver, graph_info):
    if any("p.name" in elem for elem in graph_info):
        return get_pokemon_relational_graph(driver, graph_info)
    elif any("t.name" in elem for elem in graph_info):
        return get_type_graph(driver, graph_info)
    # qui puoi aggiungere altri casi (categorie, ecc)
    else:
        # Nessun nodo grafico riconosciuto → ritorno vuoto
        return [], []

