
class WifiConfig:
    ssid: str
    password: str
    
    def __init__(self, ssid:str, password:str):
        self.ssid = ssid
        self.password = password
