import interactions as discord
import json
import cfg

class CustomClient(discord.Client):   
    config: cfg.Config = None
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        with open("config.json", "r") as f:
            self.config: cfg.Config = cfg.Config.from_dict(json.load(f))

client = CustomClient(intents=discord.Intents.GUILDS)

client.load_extensions("cogs")
    
client.start(client.config.token)