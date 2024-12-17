import interactions as discord
import config

client = discord.Client(intents=discord.Intents.GUILDS)

client.config = config.Config()
    
client.load_extensions("cogs")
    
client.start(client.config.BOT_TOKEN)