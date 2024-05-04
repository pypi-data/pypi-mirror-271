
class DiscoveryDevice:
    manufacturer = "Ellington Steanes"
    model = "v0"
    name = "_".join([manufacturer, model, "MQTT"])
    identifiers = ["id1"]
    def __init__(self, manufacturer: str, model: str, identifiers: list[str], name:str):
        self.manufacturer = manufacturer
        self.model = model
        self.identifiers = identifiers
        self.name = name
    
    def jsonPayload(self):
        return {
            "manufacturer": self.manufacturer,
            "model": self.model,
            "identifiers": self.identifiers,
            "name": self.name
        }
