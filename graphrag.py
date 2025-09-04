from utils import initialization

### Is langGraph needed? Is there a need for a llm that converts nl queries into cypher queries?
# Let's think about it:
# User write a query e.g. query_text = "Who were the actors in the movie about the magic jungle board game?"
# System performs a vector search finding match candidates, in this case Jumanji as first
# retrieval query extracts actors (since we specified it) from the graph, finding actor nodes linked to movie node
# we found both the node and its vectors/content to extract as context and additional information we required

# What we did before?
# User write a query e.g. query_text = "Which pokemon are ghost type?"
# System performs a llm call that converts nl query in cypher query matching pokemon with poke.type=Ghost
# System outputs all the nodes matched with the cypher query, saved them to context and to graph_info
# Graph info: [{'ghost_type_pokemon': 'Gastly'}, {'ghost_type_pokemon': 'Haunter'}, {'ghost_type_pokemon': 'Gengar'}]
# We later use the graph info to extract other useful info to visualize a graph (additional functions)
##### Additional info to visualize a graph extracted with a cypher query from graph info #####
# nodes = [
#     {'id': 91, 'label': 'Gastly', 'group': 'Pokemon'},
#     {'id': 92, 'label': 'Haunter', 'group': 'Pokemon'}, 
#     {'id': 93, 'label': 'Gengar', 'group': 'Pokemon'}
#     ]
# edges = [
#     {'from': 91, 'to': 92, 'label': 'EVOLVES_TO'}, 
#     {'from': 92, 'to': 91, 'label': 'EVOLVES_FROM'}, 
#     {'from': 91, 'to': 92, 'label': 'SHARE_TYPE'}, 
#     {'from': 91, 'to': 92, 'label': 'SAME_GENERATION'}, 
#     {'from': 91, 'to': 93, 'label': 'SHARE_TYPE'}, 
#     {'from': 91, 'to': 93, 'label': 'SAME_GENERATION'}, 
#     {'from': 92, 'to': 93, 'label': 'EVOLVES_TO'}, 
#     {'from': 93, 'to': 92, 'label': 'EVOLVES_FROM'}, 
#     {'from': 92, 'to': 93, 'label': 'SHARE_TYPE'}, 
#     {'from': 92, 'to': 93, 'label': 'SAME_GENERATION'}
# ]
###############################################################################################

# What are the differences?
# With VectorCypherSearch we perform just a vector search and THEN we extract other useful info with a cypher query
# e.g. query_text = "What are the ghost type pokemon?" will search for every similarity vector
# finding matches with even non-ghost type pokemon if the text content contains similar words
# we then could use the cypher query to extract linked nodes like types, categories or generation
# I am not sure if we could extract even links within the extracted nodes
# The problem here is that the BASE results are extracted via vector search (simple retrieving)
# thus reducing the accuracy of the extracted info and making more difficult to know how many matches we have to collect

# So, we should keep doing as we are currently doing, maybe using VectorCypherSearch in the place of simple VectorSearch
# We need to perform exact cypher search to retrieve exact information when asking about specific info
# But how we could enrich the results? If we simply do cypher query, in order to not ask too complex cypher queries
# to our llm we should process the content info later
# optional solution:

# we perform cypher search, extract the graph info and use them to extract all the metadata from that nodes
# and visualize the pokedex cards
# then, we pass that cards (all the retrieved pokemon info) to the llm as context to produce a satisfying response
# after that (or before idk) we call more cypher quiries to extract useful info for the graph visualization

# Important question: when do we need simple retrieval? In this case use VectorCypherSearch (or vector + external func cypher)
# e.g. "Which is the strongest pokemon?" -> this question is too general to perform a simple cypher search
# "Tell me who is the best pokemon" -> too many interpretations, best in terms of? Check if it could be 
# smart to make the llm ask for more specific details to the user, or just simply answering
# ...



retrieval_query = """
MATCH
(actor:Actor)-[:ACTED_IN]->(node)
RETURN
node.title AS movie_title,
node.plot AS movie_plot, 
collect(actor.name) AS actors;
"""

def main():

    return
