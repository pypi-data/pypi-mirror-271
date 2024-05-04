from .homeassistantdiscoveryconfig import HomeAssistantDiscoveryConfig

class MqttConfig:
    keys = [
        'host',
        'port',
        'user',
        'passwod',
        'topic_prefix',
        'location',
        'ha_discovery'
        ]
    host: str
    port: int
    user: str
    password: str
    topic_prefix: str
    location: str
    ha_discovery: HomeAssistantDiscoveryConfig

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'ha_discovery':
                self.ha_discovery = HomeAssistantDiscoveryConfig(**value)
                continue
            setattr(self, key, value)
