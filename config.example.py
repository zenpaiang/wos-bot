import interactions as discord

class Config:
    BOT_TOKEN = "" # enter your bot token here
    PLAYERS_FILE = "players.json" # path to players database
    ACTIVITY = discord.Activity(
        name="example activity",
        type=discord.ActivityType.PLAYING
    )