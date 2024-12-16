import interactions as discord

class Calculate(discord.Extension):
    @discord.slash_command(
        name="calculate",
        description="calculation related commands"
    )
    async def calculate_cmd(self, ctx: discord.SlashContext):
        pass
    
    @calculate_cmd.subcommand(
        sub_cmd_name="time",
        sub_cmd_description="calculate building time after buffs",
        options=[
            discord.SlashCommandOption(type=discord.OptionType.INTEGER, name="d", description="days", required=True, min_value=0),
            discord.SlashCommandOption(type=discord.OptionType.INTEGER, name="h", description="hours", required=True, min_value=0),
            discord.SlashCommandOption(type=discord.OptionType.INTEGER, name="m", description="minutes", required=True, min_value=0),
            discord.SlashCommandOption(type=discord.OptionType.INTEGER, name="pet_buff", description="pet buff percentage", required=True, choices=[discord.SlashCommandChoice(name=f"{v}%", value=v) for v in [0, 5, 7, 9, 12, 15]]),
            discord.SlashCommandOption(type=discord.OptionType.BOOLEAN, name="double_time", description="whether double time is active or not", required=True),
            discord.SlashCommandOption(type=discord.OptionType.INTEGER, name="external_buffs", description="external buffs percentage", required=False, min_value=0)
        ]
    )
    async def calc_buildings(self, ctx: discord.SlashContext, d: int, h: int, m: int, pet_buff: int, double_time: bool, external_buffs: int = 0):
        time_in_minutes = (d * 24 * 60) + (h * 60) + m
        
        if time_in_minutes == 0:
            await ctx.send("error: time cannot be 0")
            return
        
        if double_time:
            time_in_minutes = time_in_minutes * (80 / 100)
            
        time_in_minutes = time_in_minutes / (1 + ((pet_buff + external_buffs) / 100))
            
        days = time_in_minutes // (24 * 60)
        hours = (time_in_minutes % (24 * 60)) // 60
        minutes = time_in_minutes % 60
        
        only_hours = time_in_minutes / 60
        
        msg = (
            f"original time: {d}d {h}h {m}m\n"
            f"buffs: double time {'20%' if double_time else '0%'} | pet {pet_buff}% | external {external_buffs}% | \n"
            f"final time: {int(days)}d {int(hours)}h {int(minutes)}m | {int(only_hours)}h"
        )
        
        await ctx.send(msg)