from typing import List, TypedDict, Literal, Dict, Any
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from langchain.schema import Document
from neo4j.exceptions import SessionExpired, ServiceUnavailable, TransientError
import time

# while ($true) {
#     Start-Process -FilePath "ollama" -ArgumentList "pull mistral:7b" -NoNewWindow -Wait
#     Start-Sleep -Seconds 10
# }

def building_pokemon_graph(llm, code_llm, vectorstore, driver, NEO4J_URI, NEO4J_AUTH):

    class RoutingOutput(BaseModel):
        route_to: Literal["rag", "cypher"] =  Field(..., description="Method of answering to use.")

    class CypherQueryOutput(BaseModel):
        cypher_query: str = Field(..., description="The generated cypher query.")

    class RelationalPokemonDex(TypedDict):
        query: str
        docs: List[Document]
        cypher_query: CypherQueryOutput
        graph_info: List[Dict[str, Any]]
        prompt: str
        context: str
        response: str

    class InputState(TypedDict):
        query: str

    class OutputState(TypedDict):
        response: str
        graph_info: List[Dict[str, Any]]
        # cypher_query: CypherQueryOutput

    def route_to_cypher_or_rag(state: RelationalPokemonDex) -> str:
        query = state["query"]
        prompt = f"""
        You are an intelligent agent deciding between two methods of answering the following user question:
        "{query}"

        If the question requires a count, comparison, filtering, aggregation or sharing over the graph database, return "cypher".
        Otherwise, if it can be answered from retrieved document text, as if it's specific to a single object, return "rag".

        ### Examples
        Q: Which are the pokemon that have 2 types?
        A: cypher

        Q: Describe the appearance of Bulbasaur
        A: rag

        Q: Which pokemon is Pikachu linked to?
        A: cypher

        Q: What is the habitat of Pidgeot?
        A: rag

        Q: Which Pokemon Squirtle shares its type with?
        A: cypher

        Q: What other pokemon share the same types as Bulbasaur?
        A: cypher

        Answer with only one word: "cypher" or "rag".
        """
        retrieving_method = llm.with_structured_output(RoutingOutput)

        decision = retrieving_method.invoke(prompt)#.strip().lower()
        return decision.route_to # {"routing": decision}

    # 2. Generic RAG

    def pinecone_vector_retrieval(state: RelationalPokemonDex):
        query = state["query"]
        docs = vectorstore.similarity_search(query, k=5)
        return {"docs": docs}

    # 3. Cypher RAG

    def cypher_query_builder(state: RelationalPokemonDex):
        query = state["query"]
        system = """
    You are a Cypher expert. Given a user's question, write a Cypher query to retrieve the answer from a Pokémon knowledge graph.

    ### Graph Schema (important):
    - (:Pokemon)-[:HAS_TYPE]->(:Type {name})
    - (:Pokemon)-[:BELONGS_TO]->(:Generation {number: Int})
    - Generations are represented as integers: 1, 2, 3, ...

    ### Examples:
    Q: How many fire type pokemon are there?
    A: MATCH (p:Pokemon)-[:HAS_TYPE]->(:Type {name: "Fire"}) RETURN count(p)

    Q: How many fire type pokemon are in the first generation?
    A: MATCH (p:Pokemon)-[:HAS_TYPE]->(:Type {name: "Fire"}), (p)-[:BELONGS_TO]->(:Generation {number: 1}) RETURN count(p)

    Q: How many double type pokemon are there?
    A: MATCH (p:Pokemon)-[:HAS_TYPE]->(t:Type) WITH p, count(t) AS typeCount WHERE typeCount = 2 RETURN count(p) AS double_type_pokemon_count

    Q: Which are the pokemon that have 2 types? List both pokemon and their types.
    A: MATCH (p:Pokemon)-[:HAS_TYPE]->(t:Type) WITH p, collect(t) AS types, count(t) AS typeCount WHERE typeCount = 2 RETURN p.name, [type IN types | type.name] AS typeNames

    Q: What other pokemon share the same types as Bulbasaur?
    A: MATCH (p1:Pokemon)-[:SAME_TYPE]-(p2:Pokemon) WHERE p1.name = 'Bulbasaur' RETURN p1, p2 

    Only return the Cypher query. Do not explain anything.
    """
#MATCH (bulba:Pokemon {name: "Bulbasaur"})-[:HAS_TYPE]->(type:Type) WITH bulba, collect(DISTINCT type) AS bulbaTypes MATCH (other:Pokemon)-[:HAS_TYPE]->(type2:Type) WITH bulba, bulbaTypes, other, collect(DISTINCT type2) AS otherTypes WHERE other <> bulba AND apoc.coll.toSet(bulbaTypes) = apoc.coll.toSet(otherTypes) RETURN other.name AS pokemon_with_same_types
        full_prompt = f"{system}\n\nUser question: {query}\nCypher query:"
        output_format = code_llm.with_structured_output(CypherQueryOutput)
        cypher = output_format.invoke(full_prompt)#.strip()
        return {"cypher_query": cypher.cypher_query}


    # def run_cypher_and_format(state: RelationalPokemonDex):
    #     cypher_query = state["cypher_query"]
    #     with driver.session() as session:
    #         result = session.run(cypher_query)
    #         rows = [r.data() for r in result]
    #     formatted = "\n".join(str(r) for r in rows)
    #     return {"context": formatted}

    def run_cypher_and_format(state: RelationalPokemonDex):
        cypher_query = state["cypher_query"]
        max_retries = 3
        #driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
        # with driver.session() as session:
        #     result = session.run(cypher_query)
        #     rows = [r.data() for r in result]

        for attempt in range(max_retries):
            try:
                with driver.session() as session:
                    result = session.run(cypher_query)
                    rows = [r.data() for r in result]
                    formatted = "\n".join(str(r) for r in rows)
                    return {"context": formatted, "graph_info":rows}
            except (SessionExpired, ServiceUnavailable, TransientError) as e:
                print(f"Neo4j connection error: {e}. Retry {attempt + 1} of {max_retries}...")
                time.sleep(1 * (attempt + 1))  # backoff esponenziale semplice
        raise Exception("Max retries exceeded for Neo4j query")

    # 4. Prompt builder

    def build_prompt(state: RelationalPokemonDex):
        if "docs" in state:
            context = "\n\n".join(d.page_content for d in state["docs"])
        else:
            context = state.get("context", "")
        prompt = f"""
    You are a smart and helpful Q&A agent specialized in the pokemon knowledge, assisting users by accurately answering their questions based on the provided context.    
    Follow these steps to generate your response:
        1. Carefully review the user's query and the provided context.
        2. If the context contains just a number it means that's the answer the user is asking for.
        3. Draft a response using the selected information, ensuring the highest level of detail.
        4. Be sure to include all the information of the context in the answer.
        5. Adjust the draft to increase accuracy and relevance.
        6. Do NOT exclude any information from the provide context.
    **Context:**
    {context}
        """
        return {"prompt": prompt, "context": context}

    # 5. Answer generation

    def generate_final_answer(state: RelationalPokemonDex):
        full_prompt = state["prompt"] + "\n\nUser question: " + state["query"]
        answer = llm.invoke(full_prompt)
        return {"response": answer.content}
    

    # ACTUALLY BUILDING GRAPH
    graph = StateGraph(RelationalPokemonDex, input=InputState, output=OutputState)

    # NODES
    #graph.add_node("route_to_cypher_or_rag", route_to_cypher_or_rag)
    graph.add_node("pinecone_vector_retrieval", pinecone_vector_retrieval)
    graph.add_node("cypher_query_builder", cypher_query_builder)
    graph.add_node("run_cypher_and_format", run_cypher_and_format)
    graph.add_node("build_prompt", build_prompt)
    graph.add_node("generate_final_answer", generate_final_answer)

    # EDGES
    #graph.add_edge(START, "route_to_cypher_or_rag")
    graph.add_conditional_edges(
        START,
        route_to_cypher_or_rag,
        {
            "rag": "pinecone_vector_retrieval",
            "cypher": "cypher_query_builder"
        },
    )
    graph.add_edge("pinecone_vector_retrieval", "build_prompt")
    graph.add_edge("cypher_query_builder", "run_cypher_and_format")
    graph.add_edge("run_cypher_and_format", "build_prompt")
    graph.add_edge("build_prompt", "generate_final_answer")
    graph.add_edge("generate_final_answer", END)

    # Compile the graph
    pokemon_graph_agent = graph.compile()

    return pokemon_graph_agent

