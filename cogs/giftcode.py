from interactions.ext.paginators import Paginator
from difflib import SequenceMatcher
import interactions as discord
import hashlib
import aiohttp
import asyncio
import certifi
import json
import time
import ssl
import re

def sanitize_username(name: str) -> str:    
    return re.sub(r"^\[[A-Za-z0-9]{3}\]", "", name.replace("\u00a0", " ")).strip()

def intable(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def match_score(item: str, against: str) -> float:    
    matcher = SequenceMatcher(None)
    
    score = 0
    
    matcher.set_seqs(item, against)
    
    if " " in item:
        wordScore = 0
        
        words = item.split(" ")
        
        againstLower = against.lower()
        
        for word in words:
            if word.lower() in againstLower:
                wordScore += 1
                
        score += wordScore / len(words) * 0.6
        
    score += matcher.ratio() * 0.4
        
    return score

class Giftcode(discord.Extension):
    def __init__(self, bot: discord.Client):
        self.redeemLimits = {"inUse": False, "lastUse": 0}
        self.bot = bot
    
    async def redeem_code(self, session: aiohttp.ClientSession, code: str, player: dict) -> tuple[bool, str, str]:
        timens = time.time_ns()
        
        login_resp = await session.post(
            url="https://wos-giftcode-api.centurygame.com/api/player",
            data={
                "fid": player["id"],
                "time": timens,
                "sign": hashlib.md5(f"fid={player['id']}&time={timens}tB87#kPtkxqOS2".encode("utf-8")).hexdigest()
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            timeout=30
        )
        
        try:
            login_result = await login_resp.json()
        except Exception as _:
            return False, "error", "login error"
        
        if "msg" in login_result:
            if login_result["msg"] != "success":
                return False, "error", "login error"
        else:
            return True, None, "rate limited"
        
        timens = time.time_ns()
        
        redeem_resp = await session.post(
            url="https://wos-giftcode-api.centurygame.com/api/gift_code",
            data={
                "cdk": code,
                "fid": player["id"],
                "time": timens,
                "sign": hashlib.md5(f"cdk={code}&fid={player['id']}&time={timens}tB87#kPtkxqOS2".encode("utf-8")).hexdigest()
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            timeout=30
        )
        
        try:
            redeem_result = await redeem_resp.json()
        except Exception as _:
            return False, "error", "unknown error"
        
        if redeem_result["err_code"] == 40014:
            return True, None, "gift code does not exist"
        elif redeem_result["err_code"] == 40007:
            return True, None, "gift code has expired"
        elif redeem_result["err_code"] == 40008:
            return False, "already_claimed", "already claimed"
        elif redeem_result["err_code"] == 20000:
            return False, "successfully_claimed", "successfully claimed"
        else:
            return False, "error", "unknown error"
    
    async def recursive_redeem(self, message: discord.Message, session: aiohttp.ClientSession, code: str, players: list, counters: dict = {"already_claimed": 0, "successfully_claimed": 0, "error": 0}, recursive_depth: int = 0): # success, counters, result            
        results = {}
        
        for i in range(0, len(players), 20):
            batch = players[i:i + 20]
            
            msg = "redeeming gift code" if recursive_depth == 0 else f"redeeming gift code (retry {recursive_depth})"
            
            await message.edit(content=f"{msg}... ({min(i, len(players))}/{len(players)}) | next update <t:{1 + int(time.time()) + (len(batch) * 3)}:R>")
            
            for player in batch:
                start = time.time()
                
                exit, counter, result = await self.redeem_code(session, code, player)
                
                if exit:
                    await message.edit(content=f"error: {result}")
                    return
                else:
                    counters[counter] += 1
                    results[player["name"]] = result
                    
                await asyncio.sleep(max(0, 3 - (time.time() - start)))
                    
        remaining_players = [player for player in players if "error" in results[player["name"]]]
        
        if len(remaining_players) == 0:
            msg = (
                f"report: gift code `{code}`\n"
                f"successful: {counters['successfully_claimed']} | "
                f"already claimed: {counters['already_claimed']} | "
                f"retries: {recursive_depth}\n\n"
                f"made with ❤️ by zenpai :D"
            )
            
            await message.edit(content=msg)
            
            await session.close()
            return
                    
        await self.recursive_redeem(
            message=message,
            session=session,
            code=code,
            players=remaining_players,
            counters=counters,
            recursive_depth=recursive_depth + 1,
        )
    
    @discord.slash_command(
        name="giftcode",
        description="giftcode-related commands",
        sub_cmd_name="redeem",
        sub_cmd_description="redeem a gift code",
        options=[
            discord.SlashCommandOption(
                name="code",
                description="the code to redeem",
                required=True,
                type=discord.OptionType.STRING
            )
        ]
    )
    async def redeem(self, ctx: discord.SlashContext, code: str):
        if self.redeemLimits["inUse"]:
            await ctx.send("error: there can only be one instance of this command running at once.")
            return
        
        if self.redeemLimits["lastUse"] + 60 > time.time():
            await ctx.send("error: this command has a limit of 1 use every 1 minute to comply with WOS's rate limits.")
            return
        
        with open(self.bot.config.PLAYERS_FILE, "r") as f:
            playersObj = json.load(f)
            
        players = [{"id": key, "name": playersObj[key]} for key in playersObj]
        
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl.create_default_context(cafile=certifi.where())))
        
        message = await ctx.send("waiting...")
        
        await self.recursive_redeem(message, session, code, players)
        
        self.redeemLimits["inUse"] = False
        self.redeemLimits["lastUse"] = time.time()
    
    @discord.slash_command(
        name="giftcode",
        description="giftcode-related commands",
        group_name="users",
        group_description="user-related commands",
        sub_cmd_name="list",
        sub_cmd_description="list all users in the database"
    )
    async def list_users(self, ctx: discord.SlashContext):
        with open(self.bot.config.PLAYERS_FILE, "r") as f:
            players = json.load(f)
            
        players_list = [f"**{player_name}**" for _, player_name in players.items()]
        
        embeds_content = ["\n".join(players_list[i:i + 10]) for i in range(0, len(players_list), 10)]
        
        embeds = [
            discord.Embed(
                title="players list",
                description=f"**total players:** {len(players.items())}\n\n{content}\n\nmade with ❤️ by zenpai :D",
                color=0x4fa5fc
            ) for content in embeds_content
        ]
        
        paginator = Paginator.create_from_embeds(self.bot, *embeds, timeout=300)
        
        paginator.wrong_user_message = "error: you are not the author of this command"
        paginator.show_select_menu = False
        paginator.show_callback_button = False
        
        await paginator.send(ctx)
        
    @discord.slash_command(
        name="giftcode",
        description="giftcode-related commands",
        group_name="users",
        group_description="user-related commands",
        sub_cmd_name="add",
        sub_cmd_description="add a user to the database",
        options=[
            discord.SlashCommandOption(
                name="name",
                description="the user's name",
                required=True,
                type=discord.OptionType.STRING
            ),
            discord.SlashCommandOption(
                name="id",
                description="the user's id",
                required=True,
                type=discord.OptionType.STRING
            )
        ]
    )
    async def add(self, ctx: discord.SlashContext, name: str, id: str):    
        if intable(id):
            name = sanitize_username(name)
            
            with open(self.bot.config.PLAYERS_FILE, "r") as f:
                players = json.load(f)
                
            if id in players:
                await ctx.send("error: user already exists in the list")
                return
                
            players[id] = name
            
            with open(self.bot.config.PLAYERS_FILE, "w") as f:
                json.dump(players, f, indent=4)
                
            await ctx.send(f"added user {name} to the list.")
        else:
            await ctx.send("error: invalid user id")
            
    @discord.slash_command(
        name="giftcode",
        description="giftcode-related commands",
        group_name="users",
        group_description="user-related commands",
        sub_cmd_name="remove",
        sub_cmd_description="remove a user from the database",
        options=[
            discord.SlashCommandOption(
                name="user",
                description="the user's name",
                required=True,
                type=discord.OptionType.STRING,
                autocomplete=True
            )
        ]
    )
    async def remove(self, ctx: discord.SlashContext, user: str):
        with open(self.bot.config.PLAYERS_FILE, "r") as f:
            players = json.load(f)
            
        name = players[user]
        
        del players[user]
                
        with open(self.bot.config.PLAYERS_FILE, "w") as f:
            json.dump(players, f, indent=4)
            
        await ctx.send(f"removed user {name} from the list.")
    
    @discord.slash_command(
        name="giftcode",
        description="giftcode-related commands",
        group_name="users",
        group_description="user-related commands",
        sub_cmd_name="rename",
        sub_cmd_description="rename a user in the database",
        options=[
            discord.SlashCommandOption(
                name="name",
                description="the user's name",
                required=True,
                type=discord.OptionType.STRING,
                autocomplete=True
            ),
            discord.SlashCommandOption(
                name="new_name",
                description="the user's new username",
                required=True,
                type=discord.OptionType.STRING
            )
        ]
    )
    async def rename(self, ctx: discord.SlashContext, user: str, new_name: str):
        with open(self.bot.config.PLAYERS_FILE, "r") as f:
            players = json.load(f)
            
        new_name = sanitize_username(new_name)
            
        name = players[user]
        
        players[user] = new_name
                
        with open(self.bot.config.PLAYERS_FILE, "w") as f:
            json.dump(players, f, indent=4)
            
        await ctx.send(f"changed {name}'s name to {new_name}.")
        
    @rename.autocomplete("user")
    @remove.autocomplete("user")
    async def user_autocomplete(self, ctx: discord.AutocompleteContext):
        name = ctx.input_text
        
        with open(self.bot.config.PLAYERS_FILE, "r") as f:
            players = json.load(f)
            
        name = sanitize_username(name)
            
        results = [(player_id, player_name, match_score(name, player_name)) for player_id, player_name in players.items()]
            
        results.sort(reverse=True, key=lambda x: x[2])
        
        if not len(results):
            await ctx.send(choices=[])
            return
        
        max_score = max(results[:25], key=lambda x: x[2])[2]
        
        best_matches = [match for match in results if match[2] >= max_score * (1 - 0.3)]
        
        await ctx.send(choices=[{"name": player_name, "value": player_id} for player_id, player_name, _ in (best_matches[:25] if len(best_matches) else results[:25])])