from .disoveryDevice import DiscoveryDevice
        
class DiscoveryPayload:
    name: str
    availability_topic: str
    payload_available = "running"
    payload_not_available = "dead"
    device: DiscoveryDevice
    unique_id: str
    state_topic: str
    command_topic: str
    payload_on: str
    payload_off: str
    
    def __init__(self, name:str, availability_topic:str, payload_available: str, payload_not_available: str, device: any, unique_id: str, state_topic: str, command_topic: str, payload_on: str, payload_off: str):
        self.name = name
        self.availability_topic = availability_topic
        self.payload_available = payload_available
        self.payload_not_available = payload_not_available
        self.device = device
        self.unique_id = unique_id
        self.state_topic = state_topic
        self.command_topic = command_topic
        self.payload_on = payload_on
        self.payload_off = payload_off
    
    '''
    Should return something along the lines of:
    {
            "name": "output_name",
            "availability_topic": "availability_topic",
            "payload_available": "running",
            "payload_not_available": "dead",
            "device": {
                "manufacturer": "manufacturer_name",
                "model": "v0",
                "identifiers": [
                    "identifier_1"
                ],
                "name": "device_name"
            },
            "unique_id": "uuid",
            "state_topic": "state_topic",
            "command_topic": "command_topic",
            "payload_on": "ON",
            "payload_off": "OFF"
        }
    '''
    def return_map(self):
        return {  # Thoughts: this should be its own class and then the class has a method to return all of the key values as a json
            "name": self.name,
            "availability_topic": self.availability_topic,
            "payload_available": self.payload_available,
            "payload_not_available": self.payload_not_available,
            "device": self.device.jsonPayload(),
            "unique_id": self.unique_id,
            "state_topic": self.state_topic,
            "command_topic": self.command_topic,
            "payload_on": self.payload_on,
            "payload_off": self.payload_off
        }


class HomeAssistantDiscoveryBuilder:
    def __init__(self):
        self.name = ""
        self.availability_topic = ""
        self.payload_available = "running"
        self.payload_not_available = "dead"
        self.device = ""
        self.unique_id = ""
        self.state_topic = ""
        self.command_topic = ""
        self.payload_on = ""
        self.payload_off = ""

    def set_name(self, name):
        self.name = name
        return self

    def set_availability_topic(self, availability_topic):
        self.availability_topic = availability_topic
        return self

    def set_payload_available(self, payload_available):
        self.payload_available = payload_available
        return self

    def set_payload_not_available(self, payload_not_available):
        self.payload_not_available = payload_not_available
        return self

    def set_device(self, device):
        self.device = device
        return self

    def set_unique_id(self, unique_id):
        self.unique_id = unique_id
        return self

    def set_state_topic(self, state_topic):
        self.state_topic = state_topic
        return self

    def set_command_topic(self, command_topic):
        self.command_topic = command_topic
        return self

    def set_payload_on(self, payload_on):
        self.payload_on = payload_on
        return self

    def set_payload_off(self, payload_off):
        self.payload_off = payload_off
        return self

    def build(self):
        return DiscoveryPayload(
            self.name,
            self.availability_topic,
            self.payload_available,
            self.payload_not_available,
            self.device,
            self.unique_id,
            self.state_topic,
            self.command_topic,
            self.payload_on,
            self.payload_off
        )