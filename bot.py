from lib.client import CustomClient
from interactions import Intents

client = CustomClient(intents=Intents.GUILDS)

client.load_extensions("cogs")
    
client.start(client.config.token)