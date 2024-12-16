import interactions as discord
import json

client = discord.Client(intents=discord.Intents.GUILDS)

with open("config.json", "r") as f:
    client.CONFIG = json.load(f)
    
client.load_extensions("cogs")
    
client.start(client.CONFIG["botToken"])