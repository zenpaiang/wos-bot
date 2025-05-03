import colorama
import json
import os

colorama.init()

print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}warning: this script will overwrite your players.json file!{colorama.Style.RESET_ALL}")
input("press enter to continue or ctrl+c to cancel...")

if os.path.exists("players.json"):
    with open("players.json", "r") as f:
        old_players = json.load(f)
        
    new_players = {}
    
    for id in old_players:
        new_players[id] = {
            "name": old_players[id]["name"],
            "rank": old_players[id]["rank"],
            "discord_id": None
        }
        
    with open("players.json", "w") as f:
        json.dump(new_players, f, indent=4)
else:
    print("players.json not found, exiting...")