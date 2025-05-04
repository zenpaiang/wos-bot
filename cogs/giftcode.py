from interactions.ext.paginators import Paginator
from lib.funcs import match_score, intable
from lib.client import CustomClient
import interactions as discord
import lib.api as api
import asyncio
import json
import time
import re

def sanitize_username(name: str) -> str:    
    return re.sub(r"^\[[A-Za-z0-9]{3}\]", "", name.replace("\u00a0", " ")).strip()

class Giftcode(discord.Extension):
    def __init__(self, bot: CustomClient):
        self.bot: CustomClient = bot
        self.api = api.API()
        
    async def async_start(self):
        await self.api.init_session()
        
    def _edit_local_name(self, player_id: str, new_name: str):
        with open(self.bot.config.players_file, "r") as f:
            players = json.load(f)
            
        players[player_id]["name"] = new_name
        
        with open(self.bot.config.players_file, "w") as f:
            json.dump(players, f, indent=4)
            
    def _get_local_name(self, player_id: str) -> str:
        with open(self.bot.config.players_file, "r") as f:
            players = json.load(f)
            
        return players[player_id]["name"] if player_id in players else None
        
    async def recursive_redeem(self, message: discord.Message, code: str, players: list[tuple[str, float]], counters: dict = None, depth: int = 0):
        counters = counters or {"already_claimed": 0, "successfully_claimed": 0, "error": 0}
        
        batches = [(i, players[i:i + 20]) for i in range(0, len(players), 20)]
        
        retry = []
        
        if depth > 0:
            current_time = time.time()
            wait_time = 0
        
            for pid, last_called in players:
                ready_time = last_called + 20
                
                if current_time < ready_time:
                    wait_time += ready_time - current_time
                    current_time = ready_time
                    
                current_time += 3
        
            first_player_ready_in = players[0][1] + 20 - time.time()
            initial_wait = max(0, first_player_ready_in)
            waited_initial_wait = initial_wait == 0
        else:
            wait_time = 0
            initial_wait = 0
            waited_initial_wait = True
        
        for i, batch in batches:
            msg = "redeeming gift code" if depth == 0 else f"redeeming gift code (retry {depth})"
            
            await message.edit(content=f"{msg}... ({min(i, len(players))}/{len(players)}) | next update <t:{int(1 + time.time() + (len(batch) * 3) + wait_time)}:R>")
            
            if not waited_initial_wait:
                await asyncio.sleep(initial_wait)
                waited_initial_wait = True
            
            for player, ready in batch:
                if time.time() < (ready + 20):
                    await asyncio.sleep(ready + 20 - time.time())
                
                start = time.time()
                
                exit, counter, result, player_data = await self.api.redeem_code(code, player)
                
                if exit:
                    await message.edit(content=f"error: {result}")
                    return
                else:
                    counters[counter] += 1
                    
                    if "error" in result:
                        retry.append((player, time.time()))
                        
                    if player_data and sanitize_username(player_data["data"]["nickname"]) != self._get_local_name(player) and self.bot.config.auto_rename_users_during_redemption:
                        self._edit_local_name(player, sanitize_username(player_data["data"]["nickname"]))
                    
                await asyncio.sleep(max(0, 3 - (time.time() - start)))
        
        if len(retry) > 0:
            await self.recursive_redeem(message, code, retry, counters, depth + 1)
        else:
            msg = (
                f"report: gift code `{code}`\n"
                f"successful: {counters['successfully_claimed']} | "
                f"already claimed: {counters['already_claimed']} | "
                f"retries: {depth}\n\n"
                f"made with ❤️ by zenpai :D"
            )
            
            await message.edit(content=msg)
    
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
        if self.api.inUse:
            await ctx.send("error: the wos api is currently in use by another command")
            return
        
        if self.api.lastUsed + 60 > time.time():
            await ctx.send("error: waiting for api cooldown")
            return
        
        if self.bot.config.redeem_locked_to_admins and (int(ctx.author.id) not in self.bot.config.admins) and int(ctx.author.id) != self.bot.config.bot_owner:
            await ctx.send("error: not permitted to use this command", ephemeral=True)
            return
        
        self.api.inUse = True
        
        with open(self.bot.config.players_file, "r") as f:
            playersObj = json.load(f)
            
        players = [(player, 0) for player in list(playersObj.keys())]
        
        message = await ctx.send("waiting...")
        
        await self.recursive_redeem(message, code, players)
        
        self.api.lastUsed = time.time()
        self.api.inUse = False
    
    @discord.slash_command(
        name="giftcode",
        description="giftcode-related commands",
        group_name="users",
        group_description="user-related commands",
        sub_cmd_name="list",
        sub_cmd_description="list all users in the database"
    )
    async def list_users(self, ctx: discord.SlashContext):
        if self.bot.config.members_lock_to_admins and (int(ctx.author.id) not in self.bot.config.admins) and int(ctx.author.id) != self.bot.config.bot_owner:
            await ctx.send("error: not permitted to use this command", ephemeral=True)
            return
        
        with open(self.bot.config.players_file, "r") as f:
            players = json.load(f)
        
        rank_lists = {1: [], 2: [], 3: [], 4: [], 5: []}

        for details in players.values():
            rank_lists[details["rank"]].append(details["name"])
        
        sorted_ranks = [rank_lists[rank] for rank in range(5, 0, -1)]
        ranks = range(1, 6)
        
        rank_lines = [[] for _ in range(5)]
        
        embeds_content = []
        
        for index, rank in enumerate(sorted_ranks):
            rank_lines[index].append(f"**R{ranks[-(index + 1)]}**")
            rank_lines[index].append("")
            
            for player in rank:
                rank_lines[index].append(f"**{player}**")
                
            rank_lines[index].extend(["" for _ in range(10 - (len(rank_lines[index]) % 10))])

        lines = sum(rank_lines, [])
        
        embeds_content = ["\n".join(lines[i:i + 10]) for i in range(0, len(lines), 10)]
        
        embeds = [
            discord.Embed(
                title="players list",
                description=f"**total players:** {len(players.items())}\n\n{content}\n\nmade with ❤️ by zenpai :D",
                color=0x5865f2
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
                name="id",
                description="the user's id",
                required=True,
                type=discord.OptionType.STRING
            ),
            discord.SlashCommandOption(
                name="rank",
                description="the user's rank",
                required=True,
                type=discord.OptionType.INTEGER,
                choices=[
                    discord.SlashCommandChoice(
                        name=f"R{x + 1}",
                        value=x + 1
                    ) for x in range(5)
                ]
            ),
            discord.SlashCommandOption(
                name="discord",
                description="the user's discord user",
                required=False,
                type=discord.OptionType.USER
            )
        ]
    )
    async def add(self, ctx: discord.SlashContext, id: str, rank: int, discord: discord.User = None):
        if self.bot.config.members_lock_to_admins and (int(ctx.author.id) not in self.bot.config.admins) and int(ctx.author.id) != self.bot.config.bot_owner:
            await ctx.send("error: not permitted to use this command", ephemeral=True)
            return
        
        if intable(id):    
            with open(self.bot.config.players_file, "r") as f:
                players = json.load(f)
                
            if id in players:
                await ctx.send("error: user id already exists in the database")
                return
            
            await ctx.defer()
            
            err, _, _, user_data = await self.api.login_user(id)
            
            if not err:
                name = sanitize_username(user_data["data"]["nickname"])
                
                players[id] = {
                    "name": name,
                    "rank": rank,
                    "discord": str(discord.id) if discord else None
                }
                
                with open(self.bot.config.players_file, "w") as f:
                    json.dump(players, f, indent=4)
                    
                await ctx.send(f"added user {name} to the database")
            else:
                await ctx.send("error: api returned invalid data")
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
                name="name",
                description="the user's name",
                required=True,
                type=discord.OptionType.STRING,
                autocomplete=True,
                argument_name="id"
            )
        ]
    )
    async def remove(self, ctx: discord.SlashContext, id: str):
        if self.bot.config.members_lock_to_admins and (int(ctx.author.id) not in self.bot.config.admins) and int(ctx.author.id) != self.bot.config.bot_owner:
            await ctx.send("error: not permitted to use this command", ephemeral=True)
            return
        
        with open(self.bot.config.players_file, "r") as f:
            players = json.load(f)
            
        name = players[id]["name"]
        
        del players[id]
                
        with open(self.bot.config.players_file, "w") as f:
            json.dump(players, f, indent=4)
            
        await ctx.send(f"removed user {name} from the database")
        
    @discord.slash_command(
        name="giftcode",
        description="giftcode-related commands",
        group_name="users",
        group_description="user-related commands",
        sub_cmd_name="set_rank",
        sub_cmd_description="set a user's rank in the database",
        options=[
            discord.SlashCommandOption(
                name="name",
                description="the user's name",
                required=True,
                type=discord.OptionType.STRING,
                argument_name="id",
                autocomplete=True
            ),
            discord.SlashCommandOption(
                name="rank",
                description="the user's rank",
                required=True,
                type=discord.OptionType.INTEGER,
                choices=[
                    discord.SlashCommandChoice(
                        name=f"R{x + 1}",
                        value=x + 1
                    ) for x in range(5)
                ]
            )
        ]
    )
    async def set_rank(self, ctx: discord.SlashContext, id: str, rank: int):
        if self.bot.config.members_lock_to_admins and (int(ctx.author.id) not in self.bot.config.admins) and int(ctx.author.id) != self.bot.config.bot_owner:
            await ctx.send("error: not permitted to use this command", ephemeral=True)
            return
        
        with open(self.bot.config.players_file, "r") as f:
            players = json.load(f)
        
        players[id]["rank"] = rank
                
        with open(self.bot.config.players_file, "w") as f:
            json.dump(players, f, indent=4)
            
        await ctx.send(f"successfully set {players[id]['name']}'s rank to R{rank}", ephemeral=True)
    
    @set_rank.autocomplete("name")
    @remove.autocomplete("name")
    async def user_autocomplete(self, ctx: discord.AutocompleteContext):
        name = ctx.input_text
        
        with open(self.bot.config.players_file, "r") as f:
            players = json.load(f)
            
        name = sanitize_username(name)
            
        results = [(player_id, player_data["name"], match_score(name, player_data["name"])) for player_id, player_data in players.items()]
            
        results.sort(reverse=True, key=lambda x: x[2])
        
        if not len(results):
            await ctx.send(choices=[])
            return
        
        max_score = max(results[:25], key=lambda x: x[2])[2]
        
        best_matches = [match for match in results if match[2] >= max_score * (1 - 0.3)]
        
        await ctx.send(choices=[{"name": player_name, "value": player_id} for player_id, player_name, _ in (best_matches[:25] if len(best_matches) else results[:25])])
        
    def drop(self):
        asyncio.create_task(self.async_drop())
        super().drop()
        
    async def async_drop(self):
        await self.api.session.close()