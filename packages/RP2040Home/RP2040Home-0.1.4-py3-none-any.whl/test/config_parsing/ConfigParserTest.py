import unittest, json
from unittest.mock import mock_open, patch
from RP2040Home.configparsing.configparser import ConfigParser
from RP2040Home.configparsing.mqttconfig import MqttConfig
from RP2040Home.configparsing.output import Output
class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.config_parser = ConfigParser()

    @patch('builtins.open', new_callable=mock_open, read_data='{"pi": "wifi_config", "mqtt": {}, "digital_outputs": []}')
    def test_load_with_valid_config(self, mock_file):
        self.config_parser.load('path/to/valid/config.json')
        self.assertEqual(self.config_parser.wifi_config, "wifi_config")
        self.assertIsInstance(self.config_parser.mqtt_config, MqttConfig)
        self.assertEqual(len(self.config_parser.output_config), 0)

    @patch('builtins.open', new_callable=mock_open, read_data='{"pi": "wifi_config", "mqtt": {}, "digital_outputs": [{"name": "output1", "pin": 1, "on_payload": "ON", "off_payload": "OFF"}]}')
    def test_load_with_digital_outputs(self, mock_file):
        self.config_parser.load('path/to/valid/config_with_outputs.json')
        self.assertEqual(self.config_parser.wifi_config, "wifi_config")
        self.assertIsInstance(self.config_parser.mqtt_config, MqttConfig)
        self.assertEqual(len(self.config_parser.output_config), 1)
        self.assertIsInstance(self.config_parser.output_config[0], Output)
        self.assertEqual(self.config_parser.output_config[0].name, "output1")

    @patch('builtins.open', new_callable=mock_open, read_data='invalid_json')
    def test_load_with_invalid_json(self, mock_file):
        with self.assertRaises(json.JSONDecodeError):
            self.config_parser.load('path/to/invalid/config.json')

if __name__ == '__main__':
    unittest.main()
