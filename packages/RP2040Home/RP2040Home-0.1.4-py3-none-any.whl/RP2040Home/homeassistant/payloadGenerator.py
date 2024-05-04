from umqtt.simple import MQTTClient
from .discoveryPayload import HomeAssistantDiscoveryBuilder
from .disoveryDevice import DiscoveryDevice
from RP2040Home.configparsing.output import Output
from RP2040Home.configparsing.configparser import ConfigParser
from RP2040Home.configparsing.homeassistantdiscoveryconfig import HomeAssistantDiscoveryConfig
import json, machine, ubinascii, network

class PayloadGenerator:
    topic_prefix: str
    outputs: list[Output]
    ha_discovery: HomeAssistantDiscoveryConfig
    location: str
    UUID: str
    haDiscoveryTopics: list[str]
    
    def __init__(self, parsedConfig: ConfigParser):
        # UUID cannot contain colons from mac address https://www.home-assistant.io/integrations/mqtt/#discovery-topic
        self.UUID = "RPi2040Home-" + ubinascii.hexlify(network.WLAN().config('mac')).decode() 
        self.topic_prefix = parsedConfig.mqtt_config.topic_prefix
        self.outputs = parsedConfig.output_config
        self.ha_discovery = parsedConfig.mqtt_config.ha_discovery
        self.location = parsedConfig.mqtt_config.location
        self.haDiscoveryPayloads = []
        self.haDiscoveryTopics = []
        self.setTopicMap = {}
        if self.ha_discovery.enabled != None:
            self.createDiscoveryPayloads()

    def createDiscoveryPayloads(self) -> None:
        for output in self.outputs:
            state_topic = self.location+"/output/"+output.name
            command_topic = self.location+"/output/"+output.name+"/set"
            outputDiscoveryPayload =  HomeAssistantDiscoveryBuilder()\
            .set_name(output.name)\
            .set_availability_topic(self.topic_prefix + "/status")\
            .set_device(
                DiscoveryDevice(
                    "Home Assistant MQTT Client",
                    "v0",
                    ["Home Assistant MQTT Client", "Home Assistant MQTT Client-"+self.UUID],
                    "Home Assistant MQTT Client")
                )\
            .set_unique_id(self.UUID + "-" + output.name)\
            .set_state_topic(state_topic)\
            .set_command_topic(command_topic)\
            .set_payload_on(output.on_payload)\
            .set_payload_off(output.off_payload)\
            .build().return_map()
            self.haDiscoveryPayloads.append(outputDiscoveryPayload)
            self.setTopicMap[command_topic] = {"state_topic": state_topic, "output": output}
            self.haDiscoveryTopics.append("homeassistant/" + output.output_type + "/" + self.ha_discovery.node_id + "-" + self.UUID + "/"+output.name+"/config")
           
    def getUUID(self) -> str:
        return self.UUID
    
    def getDiscoveryPayloads(self) -> list[map]:
        return self.haDiscoveryPayloads
    
    def getDiscoveryTopics(self) -> list[str]:
        return self.haDiscoveryTopics
    
    def getSetTopicMap(self) -> map[map]:
        return self.setTopicMap
    
