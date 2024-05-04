class HomeAssistantDiscoveryConfig:
    enabled: str
    node_id: str
    
    def __init__(self, enabled:str, node_id: str):
        self.enabled = enabled
        self.node_id = node_id
