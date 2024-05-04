from RP2040Home.configparsing.configparser import ConfigParser
from RP2040Home.homeassistant.payloadGenerator import PayloadGenerator
from RP2040Home.homeassistant.mqttClient import MqttClient

import time, network, machine
from umqtt.simple import MQTTClient


class RP2040Home:
    config: ConfigParser
    def __init__(self, config:ConfigParser):
        self.config = config
        if config is None:
            raise ValueError("Config value must be set")
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.led.on()
        
    def connect_wlan(self):
        sta_if = network.WLAN(network.STA_IF)
        networkConnectTimer = 0
        if not sta_if.isconnected():
            print('Connecting to network...')
            for wifiConnection in self.config.wifi_config:
                print("Attempting to join ssid" + wifiConnection.ssid)
                sta_if.active(True)
                sta_if.connect(wifiConnection.ssid, wifiConnection.password)
                while not sta_if.isconnected() and networkConnectTimer < 30:
                    pass
                    time.sleep(1)
                    networkConnectTimer += 1
                if sta_if.isconnected():
                    break
                networkConnectTimer = 0
        print('Network config:', sta_if.ifconfig())
        return self

    def start_connection(self):
        if not network.WLAN(network.STA_IF).isconnected():
            print("Couldn't connect to any of the specified SSIDs, exiting")
            self.led.off()
            return
        
        haPayloadGenerator = PayloadGenerator(self.config)
        print(self.config.wifi_config)
        print(self.config.mqtt_config)
        print(haPayloadGenerator.getDiscoveryPayloads())
        haMqttClient = MqttClient(
            self.config.output_config,
            haPayloadGenerator.getDiscoveryPayloads(),
            haPayloadGenerator.getDiscoveryTopics(),
            haPayloadGenerator.getSetTopicMap(),
            MQTTClient(
                client_id=haPayloadGenerator.getUUID(),
                server=self.config.mqtt_config.host,
                user=self.config.mqtt_config.user,
                password=self.config.mqtt_config.password),
            machine)
        haMqttClient.mqttInitialise(True)
        
        try:
            while 1:
                haMqttClient.mqttClient.wait_msg()
        finally:
            haMqttClient.mqttStatus(False)
            haMqttClient.defaultOutputsToOff()
            haMqttClient.mqttClient.disconnect()
            self.led.off()
