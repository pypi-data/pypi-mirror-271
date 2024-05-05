class ModelInfo:
    def __init__(self, id: str, source: str, input: dict[str, str] = {},
                 output: dict[str, str] = {}) -> None:
        self.id = id
        
        if(source == "hf_model"):
            self.repo_name = id
        else:
            self.repo_name = ""
            
        self.source = source
        self.input = input
        self.output = output
        
    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, source):
        if(source != "hf_model" and source != "custom"):
            raise Exception(f"Model of type {source} not supported. Supported " +
                            "model types: hf_model, custom")
        self._source = source
        
    def __repr__(self):
        return self.id
            
        
        
        