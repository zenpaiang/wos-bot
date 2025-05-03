from interactions import Client
import lib.cfg as cfg
import json

class CustomClient(Client):   
    config: cfg.Config = None
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        with open("config.json", "r") as f:
            self.config: cfg.Config = cfg.Config.from_dict(json.load(f))