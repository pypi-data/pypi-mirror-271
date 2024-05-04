# mqtt-home
A simple micro-python mqtt client which enables simple plug-and-play functionality and interoperability with Home Assistant. 
```  
"availability_topic": "home/wateringsystem/back/status",
"state_topic": "home/wateringsystem/back/output/solenoid3",
"command_topic": "home/wateringsystem/back/output/solenoid3/set",
```

The overall standard of MQTT topics that will be used going forward is:
`<area>/<entity>/<location>/<property>/<object>/<modifier>` but there's no set requirement on structure.

topic_prefix is: `<area>/<entity>/<location>`

This simplifies it down to:
`<topic_prefix>/<property>/<object>/<modifier>`

# Software Setup
## From a fresh Raspberry Pi Pico
Following the [official Raspberry Pi Docs](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3)
1. Hold down the bootsel button while plugging in pi pico for the first time
2. Open Thonny with the pico plugged in
3. Choose the micropython language selector in the bottom right hand corner of the UI
4. Choose the latest version of Micropython and install it onto the raspberry pi
## From an existing Raspberry Pi Pico with micropython installed
5. In the top bar of Thonny, under `Tools`, there should be an option to `Manage Packages`, select that option
6. Then search for `umqtt` in the package manager, there should be one called `micropython-umqtt.simple` and install it onto the Pi Pico.
	1. You could potentially use [mpremote](https://docs.micropython.org/en/latest/reference/packages.html#installing-packages-with-mpremote) `mpremote mip install micropython-umqtt.simple` (untested) in the Thonny console when the Pi Pico is connected
8. Clone the [mqtt-home](https://github.com/ESteanes/mqtt-home) repository to a local area
9. Create an appropriate `config.json` file based off the `test-config.json`
10. Upload `config.json`, `main.py`, `boot.py` and `main` to the Pi Pico
11. Manually run `boot.py` and `main.py` in Thonny to ensure that the SSID and password are correct, in addition to the Home Assistant connection.
12. Once confirmed connected, disconnect the Pi Pico and plug it in from cold to ensure that the start up works as expected.
13. Once the status LED is shining, that is an indication that `main.py` is running and the Pi Pico should be up and running!

## Virtual Environment Setup
* Using a virtual environment, install the python dependencies listed in `requirements.txt` by running `python -m pip install -r requirements.txt`
