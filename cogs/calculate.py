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
        
    @calculate_cmd.subcommand(
        sub_cmd_name="resources",
        sub_cmd_description="calculate how to distribute queues",
        options=[
            discord.SlashCommandOption(type=discord.OptionType.STRING, name="meat", description="amount of meat you have", required=True),
            discord.SlashCommandOption(type=discord.OptionType.STRING, name="wood", description="amount of wood you have", required=True),
            discord.SlashCommandOption(type=discord.OptionType.STRING, name="coal", description="amount of coal you have", required=True),
            discord.SlashCommandOption(type=discord.OptionType.STRING, name="iron", description="amount of iron you have", required=True),
            discord.SlashCommandOption(
                type=discord.OptionType.INTEGER,
                name="level",
                description="level of gathering node",
                required=True,
                choices=[
                    discord.SlashCommandChoice(
                        name=f"Level {x + 1}",
                        value=x
                    ) for x in range(8)
                ]
            ),
            discord.SlashCommandOption(
                type=discord.OptionType.INTEGER,
                name="queues",
                description="number of queues",
                required=True,
                max_value=6,
                min_value=1
            )
        ]
    )
    async def calc_resources(self, ctx: discord.SlashContext, meat: str, wood: str, coal: str, iron: str, level: int, queues: int):
        def floatable(s: str) -> bool:
            try:
                float(s)
                return True
            except Exception as _:
                return False
        
        def parse_resource_value(value) -> tuple[bool, float]:
            multipliers = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}
            
            if value[-1].lower() in multipliers:
                return True, int(float(value[:-1]) * multipliers[value[-1].lower()])
            elif floatable(value):
                return True, int(value)
            else:
                return False, 0.0
            
        def format_number(num):
            if num >= 1_000_000_000:
                return f"{num / 1_000_000_000:.1f}B"
            elif num >= 1_000_000:
                return f"{num / 1_000_000:.1f}M"
            elif num >= 1_000:
                return f"{num / 1_000:.1f}K"
            return str(num)
            
        meat_valid, meat_parsed = parse_resource_value(meat)
        wood_valid, wood_parsed = parse_resource_value(wood)
        coal_valid, coal_parsed = parse_resource_value(coal)
        iron_valid, iron_parsed = parse_resource_value(iron)
        
        if not all([meat_valid, wood_valid, coal_valid, iron_valid]):
            await ctx.send("error: invalid resource values")
            return
        
        CAPACITIES = {
            "meat": [70000, 150000, 300000, 600000, 1200000, 3000000, 6000000, 14000000],
            "wood": [70000, 150000, 300000, 600000, 1200000, 3000000, 6000000, 14000000],
            "coal": [14000, 30000, 60000, 120000, 240000, 600000, 1200000, 2800000],
            "iron": [3500, 7500, 15000, 30000, 60000, 150000, 300000, 700000]
        }
        
        target_ratio = {"meat": 20, "wood": 20, "coal": 4, "iron": 1}
        
        user_resources = {
            "meat": meat_parsed,
            "wood": wood_parsed,
            "coal": coal_parsed,
            "iron": iron_parsed
        }
        
        user_resources_equalized = { resource: user_resources[resource] * 20 / target_ratio[resource] for resource in user_resources }

        target_resource = max(user_resources_equalized, key=user_resources_equalized.get)
        
        deficiencies_equalized = { resource: user_resources_equalized[target_resource] - user_resources_equalized[resource] for resource in user_resources_equalized }
        
        gatherings = { resource: deficiencies_equalized[resource] / (CAPACITIES[resource][level] * 20 / target_ratio[resource]) for resource in deficiencies_equalized }
        raw_gatherings_queues = { resource: gatherings[resource] / sum(gatherings.values()) * queues for resource in gatherings }
        floored_queues = { resource: int(raw_gatherings_queues[resource]) for resource in raw_gatherings_queues }
        remainders = { resource: raw_gatherings_queues[resource] - floored_queues[resource] for resource in raw_gatherings_queues }
        remaining = queues - sum(floored_queues.values())
        sorted_resources = sorted(remainders, key=remainders.get, reverse=True)
        
        for resource in sorted_resources:
            if remaining == 0:
                break
            floored_queues[resource] += 1
            remaining -= 1
        
        after = { resource: user_resources[resource] + (floored_queues[resource] * CAPACITIES[resource][level]) for resource in user_resources }
        
        total_allocated = sum(after.values())
        actual_ratios = { resource: after[resource] / total_allocated * sum(target_ratio.values()) for resource in after }
        deviations = { resource: (actual_ratios[resource] - target_ratio[resource]) / target_ratio[resource] for resource in target_ratio }
        
        total_deviation = sum(abs(deviations[resource]) / 4 for resource in deviations) * 100
        
        embed = discord.Embed(
            color=0xcb00ff,
            title="queue distribution",
            description=f"**deviation:** {total_deviation:.2f}%"
        )
        
        embed.add_field(
            name="queues",
            value="\n".join([f"**{resource}:** {floored_queues[resource]}" for resource in floored_queues]),
            inline=True
        )
        
        embed.add_field(
            name="after",
            value="\n".join([f"**{resource}:** {format_number(after[resource])}" for resource in after]),
            inline=True
        )
        
        await ctx.send(embed=embed)