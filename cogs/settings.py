from lib.client import CustomClient
import interactions as discord
import json
import re

regex = re.compile(r"settings_(\d)")

class Configuration(discord.Extension):
    def __init__(self, bot: CustomClient):
        self.bot: CustomClient = bot
        
    def save_config(self):
        with open("config.json", "w") as f:
            json.dump(self.bot.config.to_dict(), f, indent=4)
        
    def _c(self, b: bool):
        return discord.ButtonStyle.SUCCESS if b else discord.ButtonStyle.DANGER
    
    def generate_ui(self) -> tuple[discord.Embed, list[discord.Button]]:
        embed = discord.Embed(title="Settings",color=0x5865f2)
        embed.add_field(name="1. auto rename users during redemption", value="`true`" if self.bot.config.auto_rename_users_during_redemption else "`false`", inline=True)
        embed.add_field(name="2. sync discord usernames", value="`true`" if self.bot.config.sync_discord_usernames else "`false`", inline=True)
        embed.add_field(name="3. /redeem locked to admins", value="`true`" if self.bot.config.redeem_locked_to_admins else "`false`", inline=True)
        embed.add_field(name="4. member editing lock to admins", value="`true`" if self.bot.config.members_lock_to_admins else "`false`", inline=True)
        embed.set_footer(text="made with ❤️ by zenpai")
        
        toggles = [
            discord.Button(
                style=self._c(a),
                label=f"{i + 1}",
                custom_id=f"settings_{i + 1}",
            ) for i, a in enumerate([
                self.bot.config.auto_rename_users_during_redemption,
                self.bot.config.sync_discord_usernames,
                self.bot.config.redeem_locked_to_admins,
                self.bot.config.members_lock_to_admins
            ])
        ]
        
        components = [discord.ActionRow(*toggles)]
        
        return embed, components
        
    @discord.slash_command(
        name="admin",
        description="wos-bot admin commands",
        sub_cmd_name="settings",
        sub_cmd_description="configure wos-bot settings",
    )
    async def settings(self, ctx: discord.SlashContext):
        if (int(ctx.author.id) not in self.bot.config.admins) and int(ctx.author.id) != self.bot.config.bot_owner:
            await ctx.send("error: not permitted to use this command", ephemeral=True)
            return
        
        embed, components = self.generate_ui()
        
        await ctx.send(embed=embed, components=components, ephemeral=True)
        
    @discord.component_callback(regex)
    async def settings_callback(self, ctx: discord.ComponentContext):
        if (int(ctx.author.id) not in self.bot.config.admins) and int(ctx.author.id) != self.bot.config.bot_owner:
            await ctx.send("error: not permitted to use this command", ephemeral=True)
            return
        
        index = int(ctx.custom_id.split("_")[1]) - 1
        
        if index == 0:
            self.bot.config.auto_rename_users_during_redemption = not self.bot.config.auto_rename_users_during_redemption
        elif index == 1:
            self.bot.config.sync_discord_usernames = not self.bot.config.sync_discord_usernames
        elif index == 2:
            self.bot.config.redeem_locked_to_admins = not self.bot.config.redeem_locked_to_admins
        elif index == 3:
            self.bot.config.members_lock_to_admins = not self.bot.config.members_lock_to_admins
            
        self.save_config()
        
        embed, components = self.generate_ui()
        
        await ctx.edit_origin(embed=embed, components=components)
        
    @discord.slash_command(
        name="admin",
        description="wos-bot admin commands",
        sub_cmd_name="add",
        sub_cmd_description="add a user to the admin list",
        options=[
            discord.SlashCommandOption(
                name="user",
                type=discord.OptionType.USER,
                description="user to add to the admin list",
                required=True
            )
        ]
    )
    async def add(self, ctx: discord.SlashContext, user: discord.User):
        if (int(ctx.author.id) not in self.bot.config.admins) and int(ctx.author.id) != self.bot.config.bot_owner:
            await ctx.send("error: not permitted to use this command", ephemeral=True)
            return
        
        if int(user.id) in self.bot.config.admins:
            await ctx.send("error: user is already an admin", ephemeral=True)
            return
        
        self.bot.config.admins.append(int(user.id))
        
        self.save_config()
        
        await ctx.send("successfully added user to the admin list", ephemeral=True)
        
    @discord.slash_command(
        name="admin",
        description="wos-bot admin commands",
        sub_cmd_name="remove",
        sub_cmd_description="remove a user from the admin list",
        options=[
            discord.SlashCommandOption(
                name="user",
                type=discord.OptionType.USER,
                description="user to remove from the admin list",
                required=True
            )
        ]
    )
    async def remove(self, ctx: discord.SlashContext, user: discord.User):
        if (int(ctx.author.id) not in self.bot.config.admins) and int(ctx.author.id) != self.bot.config.bot_owner:
            await ctx.send("error: not permitted to use this command", ephemeral=True)
            return
        
        if int(user.id) not in self.bot.config.admins:
            await ctx.send("error: user is not an admin", ephemeral=True)
            return
        
        self.bot.config.admins.remove(int(user.id))
        
        self.save_config()
        
        await ctx.send("successfully removed useer from the admin list", ephemeral=True)