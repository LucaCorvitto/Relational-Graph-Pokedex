# Welcome to Relational Graph Pokédex!
This is a fun made project (pun intended!) to test out Knowledge Graphs capabilities and GraphRAG.
It's a work in progress, so everything can change, from the UI to the core features, I just need to figure out what I want and make it!

## Current Features
* **RAG Search**: ask about your favorite pokemon and see what information are registered in our Pokedex!
* **Knowledge Graph Search**: ask about specific information regardin specific pokemons, types or generation and let our Pokedex search the right information and relations for you! It could be a mere number or an entire graph!
* **Graph Visualization**: Whether your question regards some relationships between pokemon, take a look at how different pokemon are related based on evolutions, type or generations! You can even touch the pokemon (nodes) you are interested in and highlight their relationships.

## DEMO
Working on a video demonstration of the current features of the app.

## Current relations
Still limited to the first generation and on the current relationships:
* `BELONGS_TO` -> node `Category`:`Legendary`
* `BELONGS_TO` -> node `Category`:`Starter`
* `BELONGS_TO` -> node `Category`:`Fossil`
* `BELONGS_TO` -> node `Category`:`Mythical`
* `SHARE_CATEGORY` (no additional info on the specific category)
* `HAS_TYPE` -> node `Type: <type>`
* `SAME_TYPE` -> node `Pokémon: <name>` (label specific type)
* `SAME_GENERATION` -> node `Pokémon: <name>`
* `EVOLVES_TO` -> node `Pokémon: <name>`
* `EVOLVES_FROM` -> node `Pokémon: <name>`
* `BELONGS_TO_GEN` -> node `Generation: <gen>`
* `WEAK_TO` -> node `Type: <type>`
* `RESISTENT_TO` -> node `Type: <type>`
* `IMMUNE_TO` -> node `Type: <type>`

# COME AVVIARE
apri il terminale
scrivi: $env:OLLAMA_HOST="127.0.0.1:11435"
poi: ollama serve

## TODO
### Models
Model to download and test:
needed to make it work for now:
* ollama pull llama3.1:8b (general)
* ollama pull qwen2.5-coder:7b (coding-cypher)
* ollama pull dengcao/Qwen3-Embedding-0.6B:F16 (embedding-simple rag)
other potential models
* general tasks
  * ollama pull deepseek-r1:8b
  * ollama pull gemma3n:e4b
  * ollama pull gemma3:4b
  * ollama pull llama3.1:8b
  * ollama pull llama3.2:3b
* coding
  * ollama pull codellama:7b
  * ollama pull qwen2.5-coder:7b
  * ollama pull starcoder2:7b
* tool use / rag
  * ollama pull command-r7b
  * ollama pull mistral:7b

### Features
Follow the order of implementation, first enlarge the KG and then edit the langgraph process.

Add cards of different types related to the performed search (pokemon card, type card etc), cards explodes on mouse hover or click.

#### Knowledge Graph
##### DONE
* Update the Knowledge Graph adding new relationships and using more specific ones, like:
  * `BELONGS_TO_GEN`
  * `WEAK_TO`
  * `RESISTENT_TO`
  * `IMMUNE_TO`
* and add labels to generic relationships, like:
`CREATE (p1)-[:SHARE_TYPE {type: "Electric"}]->(p2)` and then return the label from the call

```
MATCH (p1)-[r:SHARE_TYPE]->(p2)
RETURN p1.name AS from, p2.name AS to, r.type AS label
```

This can make easier to search for specific type sharing:

```
MATCH (p1:Pokemon)-[r:SHARE_TYPE]->(p2:Pokemon)
WHERE r.type = ["Electric"]
RETURN p1.name, p2.name
```
##### not done
* Update the Knowledge Graph adding new relationships between Types:
  * `WEAK_TO`
  * `RESISTENT_TO`
  * `IMMUNE_TO`
  * `SUPER_EFFECTIVE_TO` (give this to pokemon too after a check if at least one of the type is super effective to one of the two types of the other pokemon and is not weak or immune to the other type)
Extract these info from the type effectiveness table.

* Update the DataBase enhancing the information extraction from the websites including also:
  * Pokedex entry relative to their generation (or every gen)
  * General information (height, weight, etc)
  * Including abilities can lead to having to create other links like SHARE_ABILITY
  * Game Stats (Atk, Def, SpAtk, SpDef...) (forse troppo meta)
  * Game locations (idk)
  #### done
  * General info and additional effects sections of Type nodes e.g. look [here](https://bulbapedia.bulbagarden.net/wiki/Fire_(type))
  * General info and terminology sections for category nodes, pay attention that starter -> [first partner pokemon](https://bulbapedia.bulbagarden.net/wiki/First_partner_Pok%C3%A9mon), and that fossil is just fossil (not fossil pokemon)
#### LangGraph Process
**IMPORTANT**: check how [hybridsearch](https://neo4j.com/blog/developer/hybrid-retrieval-graphrag-python-package/) could be performed if useful.
Check `neo4j_graphrag_pipeline.ipynb` to see how to implement vectorcyphersearch.

The following are edits that can be done at the same time, changing the flow of the app with rag-cypherRag-graphTraversal. The graphTraversal phase is done to enlarge the context, and can be exploited to retrieve more and tailored information for the graph visualization. Extracting info from the query could be interesting:
* Add Graph Visualization for every request, update and create new graph building functions
* Extract information directly from the query, to understand what the user is asking and plot the right graph (Take pokemon names, types, relationships etc)
* Extract information from the rag output, building a graph in any case
* Change the workflow of the application, from deciding if perform rag or cypher rag to perform both with graph traversal (vectorcyphersearch perform simple retrieving + additional metadata/linked nodes requested, it should be similar, or even better, than graph traversal for our task)
* Add a graph traversal algorithm like PPR (how to personalize weights?) to reach linked nodes and enlarge the information extracted.

##### How to do it
**Notice**: we are going to take a different approach:
Noting that:
* We need to perform exact cypher search to retrieve exact information when asking about specific info like:
  * exact Type/Pokemon/other relation
  * count
* We still need to perform vector search for more general questions like:
  * Which is the strongest pokemon?
  * Tell me who is the best pokemon in terms of breeding

We should keep the distinction between answering with a cypher search and a vector search, but we are going to enrich the context in bot cases, following these steps:
* Perform retrieval/search to extract all the needed info and visualize the pokemon/dex cards 
* Pass that info to the llm to produce a satisfying response
(check if it's possible to do it in parallel, otherwise collect the llm response and visualize it (writing it down progressively) while proceeding with the next process)
* call other cypher queries to collect info for the graph visualization

The difference between general and specific questions will lies in the first step:
* Specific question: cypher search with extraction of all linked metadata
* General question: vector search with cypher extraction of all linked metadata (located the nodes with vector search we can access to their metadata, check if it's possible to do so with simple neo4j graphrag vector search)

To visualize a graph (and pokemon/dex cards) even when no output nodes are required (e.g. a count) we will let the model do a different cypher query outputting a list of nodes and then visualize graphs with additional functions.
To visualize a graph based on the nodes listed in the output, we have to check the values of the keys:
  * if value is a pokemon visualize the graph of the pokemon and links (choose how many, like a top-k)
  * if value is a type visualize links between the types
  * if value is a category visualize all the pokemon that belongs to that category (links)
e.g. query is "How many fire type pokemon are there?":
* classic output is count(pokemon with fire type in types) OR count(pokemon nodes linked to fire type node)
* we edit the cypher query (or create another one) to output `pokemon with fire type in types` OR `pokemon nodes linked to fire type node` and then perform count on the list
* alternatively we analyze the query and perform another cypher query based on result of the analysis (fire type found, search for Fire type and its links)


### UI
* Update the UI and UX, from just a pokedex to a richer interface, older IDEAS:
  * Keep the pokedex on the side (right or left) and let visualize the images of the output pokemon instead of the graph in it, on the other side let's visualize different graphs highlighting different relationships between the search pokemon. We can make a single pokedex but that can be opened up, it's close in the mobile version and open in the desktop one
  * Reject the standard pokedex idea and make a UI that is wider and chat-simile but still resembles a pokedex, add then graph visualizer on the side if requests.
#### work in progress
  * keep the queries on the page route so, in the future - if starts_with "/query=" and ends_with "=NEW", generate a new query, while if it ends_with "a random 4 digit code": access the database for that query. This is to be able to obtain a share link with other people.
