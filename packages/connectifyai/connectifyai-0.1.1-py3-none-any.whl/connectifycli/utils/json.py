from connectifycli.graph.graph import Graph
from connectifycli.graph.model_info import ModelInfo

# input: graph json from database
# output: Graph object filled with ModelInfo
def convert_to_graph(input_json):
    
    if(input_json.get('graph') is None):
        raise Exception("No graph provided in json")
    
    input_graph: dict = input_json.get('graph')
    if(input_graph == None):
        print("Json provided improper format")
    
    input_nodes: list[dict] = input_graph.get('nodes')
    input_edges: list[dict] = input_graph.get('edges')
    
    if(input_nodes == None or input_edges == None):
        print("Json provided has no nodes or edges")
        
    graph: Graph = Graph()
        
    for node in input_nodes:
        source: str = "hf_model"
        id: str = node.get("repoId")
        
        graph.add_node(ModelInfo(id, source, {}, {}))
        
    for edge in input_edges:
        source_id: str = edge["sourceNode"]["repoId"]
        dest_id: str = edge["targetNode"]["repoId"]
        
        graph.add_edge(source_id, dest_id)
    
    return graph
        