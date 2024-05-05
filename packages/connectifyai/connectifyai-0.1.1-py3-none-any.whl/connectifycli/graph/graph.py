from typing import Optional
from connectifycli.graph.model_info import ModelInfo
from collections import deque

class Graph:

    def __init__(self) -> None:
        self.nodes: dict[ModelInfo, set[ModelInfo]] = {}
        
    @property
    def models(self):
        return self.nodes.keys()
    
    @property
    def edges(self) -> dict[ModelInfo, set]:
        return self.nodes
    
    def add_node(self, model: ModelInfo) -> None:
        if(model in self.nodes.keys()):
            raise Exception(f"Attempting to add duplicate model {model}")
        for model_info in self.nodes.keys():
            if(model.id == model_info.id):
                raise Exception(f"Attempting to add duplicate model ID {model.id}")
            
        self.nodes[model] = set()
        
    def add_edge(self, source: str, dest: str) -> None:
        if(source == dest):
            raise Exception("Attempting to add edge to itself")
        source_model: Optional[ModelInfo] = None
        dest_model: Optional[ModelInfo] = None
        for i, model in enumerate(self.nodes.keys()):
            if(model.id == source):
                source_model = model
            elif(model.id == dest):
                dest_model = model
        
        if(source_model is None):
            raise Exception(f"{source} node not found in graph")
        if(dest_model is None):
            raise Exception(f"{dest} node not found in graph")
        
        if(dest_model in self.nodes[source_model]):
            raise Exception(f"Adding {source} to {dest} edge to graph, which" +
                            " already exists")           
        self.nodes[source_model].add(dest_model)
        
    def __str__(self) -> str:
        string: str = ""
        for i, model in enumerate(self.nodes.keys()):
            string += f"{model.id}:"
            for dest in self.nodes[model]:
                string += dest.id
            string += "\n"
            
        return string.rstrip()
    
    def get_model_info(self, id: str) -> Optional[ModelInfo]:
        for model_info in self.nodes.keys():
            if id == model_info.id:
                return model_info
        return None
    
    def linear_path(self) -> list[ModelInfo]:
        stack: deque = deque()
        visited: dict[ModelInfo, int] = {}
        
        for model_info in self.nodes.keys():
            visited[model_info] = 0
            
        for model_info in self.nodes.keys():
            if not visited[model_info]:
                self.dfs(model_info, visited, stack)
            
        path: list[ModelInfo] = list(stack)
        path.reverse()
        return path
        
    def dfs(self, model: ModelInfo, visited: dict[ModelInfo, int], stack: deque):
        visited[model] = -1
        
        for dest_model in self.nodes[model]:
            if visited[dest_model] == -1:
                raise Exception("Graph is not acyclic. Linear path cannot be found.")
            if visited[dest_model] == 0:
                self.dfs(dest_model, visited, stack)
                
        visited[model] = 1
        stack.append(model)
        
    
        
    

        