import interactions as discord
import config
import json

client = discord.Client(intents=discord.Intents.GUILDS)

client.config = config.Config()

# checker + migrator (will be removed in future update)

with open(client.config.PLAYERS_FILE, "r") as f:
    players = json.load(f)
    
    if players:
        if not isinstance(players[list(players.keys())[0]], dict):
            print("migrating to v2 format...")
            
            new_players = {}

            for uid in players:
                new_players[uid] = {
                    "name": players[uid],
                    "rank": 0
                }
                
            new = open("players.json", "w")
            json.dump(new_players, new, indent=4)
            new.close()
            
            print("successfully migrated to v2")

@discord.listen()
async def on_ready():
    if client.config.ACTIVITY:
        await client.change_presence(activity=client.config.ACTIVITY)
    
client.load_extensions("cogs")
    
client.start(client.config.BOT_TOKEN)