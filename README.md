# Welcome to Relational Graph Pokédex!
This is a fun made project (pun intended!) to test out Knowledge Graphs capabilities and GraphRAG.
It's a work in progress, so everything can change, from the UI to the core features, I just need to figure out what I want and make it!

## Current Features
* **RAG Search**: ask about your favorite pokemon and see what information are registered in our Pokedex!
* **Knowledge Graph Search**: ask about specific information regardin specific pokemons, types or generation and let our Pokedex search the right information and relations for you! It could be a mere number or an entire graph!
* **Graph Visualization**: Whether your question regards some relationships between pokemon, take a look at how different pokemon are related based on evolutions, type or generations! You can even touch the pokemon (nodes) you are interested in and highlight their relationships.

## DEMO
Working on a video demonstration of the current features of the app.

## Limitations
Still limited to the first generation and on the current relationships:
* `BELONGS_TO` -> node `Generation`
* `BELONGS_TO` -> node `Category`:`Legendary`
* `BELONGS_TO` -> node `Category`:`Starter`
* `BELONGS_TO` -> node `Category`:`Fossil`
* `BELONGS_TO` -> node `Category`:`Mythical`
* `SHARE_CATEGORY` (no additional info on the specific category)
* `HAS_TYPE`
* `SAME_TYPE`
* `SAME_GENERATION`
* `EVOLVES_TO`
* `EVOLVES_FROM`


## TODO
### Models
Model to download and test:
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
#### Knowledge Graph
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
WHERE r.types = ["Electric"]
RETURN p1.name, p2.name
```
* Update the DataBase enhancing the information extraction from the websites including also:
  * Pokedex entry relative to their generation (or every gen)
  * General information (height, weight, etc)
  * Game Stats (Atk, Def, SpAtk, SpDef...)
  * Game locations (idk)
#### LangGraph Process
The following are edits that can be done at the same time, changing the flow of the app with rag-cypherRag-graphTraversal. The graphTraversal phase is done to enlarge the context, and can be exploited to retrieve more and tailored information for the graph visualization. Extracting info from the query could be interesting:
* Add Graph Visualization for every request, update and create new graph building functions
* Extract information directly from the query, to understand what the user is asking and plot the right graph (Take pokemon names, types, relationships etc)
* Extract information from the rag output, building a graph in any case
* Change the workflow of the application, from deciding if perform rag or cypher rag to perform both with graph traversal
### UI
* Update the UI and UX, from just a pokedex to a richer interface, IDEAS:
  * Keep the pokedex on the side (right or left) and let visualize the images of the output pokemon instead of the graph in it, on the other side let's visualize different graphs highlighting different relationships between the search pokemon. We can make a single pokedex but that can be opened up, it's close in the mobile version and open in the desktop one
  * Reject the standard pokedex idea and make a UI that is wider and chat-simile but still resembles a pokedex, add then graph visualizer on the side if requests. 

