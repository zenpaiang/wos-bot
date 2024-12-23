import interactions as discord
import config

client = discord.Client(intents=discord.Intents.GUILDS)

client.config = config.Config()

@discord.listen()
async def on_ready():
    if client.config.ACTIVITY:
        await client.change_presence(activity=client.config.ACTIVITY)
    
client.load_extensions("cogs")
    
client.start(client.config.BOT_TOKEN)