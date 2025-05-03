import interactions as discord
from lib.funcs import match_score
import json

class Database(discord.Extension):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        
        with open("database/chief_gear.json", "r") as f:
            self.databaseChiefGear = json.load(f)
            
        with open("database/chief_charm.json", "r") as f:
            self.databaseChiefCharm = json.load(f)
            
        with open("database/fire_crystals.json", "r") as f:
            self.databaseFireCrystals = json.load(f)
    
    @discord.slash_command(
        name="database",
        description="all database related commands"
    )
    async def database_cmd(self, ctx: discord.SlashContext):
        pass
    
    @database_cmd.subcommand(
        sub_cmd_name="chief_gear",
        sub_cmd_description="chief gear database",
        options=[
            discord.SlashCommandOption(
                type=discord.OptionType.STRING,
                name="type",
                description="chief gear type",
                choices=[
                    discord.SlashCommandChoice(
                        name=i.capitalize(),
                        value=i
                    ) for i in ["coat", "hat", "pants", "ring", "staff", "watch"]
                ],
                required=True
            ),
            
            discord.SlashCommandOption(
                type=discord.OptionType.STRING,
                name="rarity",
                description="chief gear rarity",
                autocomplete=True,
                required=True
            ),
            
            discord.SlashCommandOption(
                type=discord.OptionType.STRING,
                name="current",
                description="the current rarity of your chief gear",
                autocomplete=True,
                required=False
            )
        ]
    )
    async def chief_gear(self, ctx: discord.SlashContext, type: str, rarity: str, current: str = None):
        types = {
            "hat": "Lancer",
            "watch": "Lancer",
            "coat": "Infantry",
            "pants": "Infantry",
            "ring": "Marksman",
            "staff": "Marksman"
        }

        if "uncommon" in rarity:
            color = 0x1ab538
        elif "rare" in rarity:
            color = 0x5fb0f5
        elif "epic" in rarity:
            color = 0xa461f7
        elif "mythic" in rarity:
            color = 0xf59b5f
            
        stats = self.databaseChiefGear[rarity]["stats"]
        
        url = f"https://raw.githubusercontent.com/zenpaiang/wos-database/refs/heads/master/chief_gear/{rarity}/{type}.png"
        
        embed = discord.Embed(title=f"{self.databaseChiefGear[rarity]['name']}", color=color)
        
        embed.add_field("Stats", f"{types[type]} Defense: {stats}%\n{types[type]} Attack: {stats}%\n\n{self.databaseChiefGear[rarity]['power']} <:power:1316326705346121738>", inline=True)
        
        if current:
            dictKeys = list(self.databaseChiefGear.keys())
            
            totalCostCurrent = {"hardened_alloy": 0, "polishing_solution": 0, "design_plans": 0, "amber": 0}
            
            for key in dictKeys[:dictKeys.index(current) + 1]:
                costDict = self.databaseChiefGear[key]["cost"]
                
                totalCostCurrent["hardened_alloy"] += costDict["hardened_alloy"]
                totalCostCurrent["polishing_solution"] += costDict["polishing_solution"]
                totalCostCurrent["design_plans"] += costDict["design_plans"]
                totalCostCurrent["amber"] += costDict["amber"]
                
            totalCostToGet = {"hardened_alloy": 0, "polishing_solution": 0, "design_plans": 0, "amber": 0}
            
            for key in dictKeys[:dictKeys.index(rarity) + 1]:
                costDict = self.databaseChiefGear[key]["cost"]
                
                totalCostToGet["hardened_alloy"] += costDict["hardened_alloy"]
                totalCostToGet["polishing_solution"] += costDict["polishing_solution"]
                totalCostToGet["design_plans"] += costDict["design_plans"]
                totalCostToGet["amber"] += costDict["amber"]
                
            totalCostToGet = {
                "hardened_alloy": totalCostToGet["hardened_alloy"] - totalCostCurrent["hardened_alloy"], 
                "polishing_solution": totalCostToGet["polishing_solution"] - totalCostCurrent["polishing_solution"], 
                "design_plans": totalCostToGet["design_plans"] - totalCostCurrent["design_plans"], 
                "amber": totalCostToGet["amber"] - totalCostCurrent["amber"]
            }
            
            embed.add_field(f"Materials Needed (from {self.databaseChiefGear[current]['name']})", f"{totalCostToGet['hardened_alloy']} <:iron:1310197207097413652>\n{totalCostToGet['polishing_solution']} <:polishing_solution:1310197178244927548>\n{totalCostToGet['design_plans']} <:design_plan:1310197143230877758>\n{totalCostToGet['amber']} <:amber:1316330006703771688>", inline=True)
        
        embed.set_thumbnail(url)
        embed.set_footer("powered by wos-database 💖")
        
        await ctx.send(embed=embed)
    
    @chief_gear.autocomplete("current")
    @chief_gear.autocomplete("rarity")
    async def chief_gear_autocomplete(self, ctx: discord.AutocompleteContext):
        input = ctx.input_text
        
        results = [(id, match_score(input, id)) for id in self.databaseChiefGear]
            
        results.sort(reverse=True, key=lambda x: x[1])
        
        max_score = max(results[:25], key=lambda x: x[1])[1]
        
        best_matches = [match for match in results if match[1] >= max_score * (1 - 0.3)]
        
        await ctx.send(choices=[{"name": self.databaseChiefGear[match[0]]["name"], "value": match[0]} for match in (best_matches[:25] if len(best_matches) else results[:25])])
        
    @database_cmd.subcommand(
        sub_cmd_name="chief_charm",
        sub_cmd_description="chief charm database",
        options=[
            discord.SlashCommandOption(
                name="level",
                description="chief charm level",
                type=discord.OptionType.INTEGER,
                choices=[
                    discord.SlashCommandChoice(
                        name=f"Lvl. {i + 1}",
                        value=i + 1
                    ) for i in range(11)
                ],
                required=True
            ),
            
            discord.SlashCommandOption(
                name="type",
                description="chief charm type",
                type=discord.OptionType.STRING,
                choices=[
                    discord.SlashCommandChoice(
                        name="Keenness (Lancer)",
                        value="keenness"
                    ),
                    
                    discord.SlashCommandChoice(
                        name="Protection (Infantry)",
                        value="protection"
                    ),
                    
                    discord.SlashCommandChoice(
                        name="Vision (Marksman)",
                        value="vision"
                    )
                ],
                required=True
            ),
            
            discord.SlashCommandOption(
                name="current",
                description="your current chief charm",
                type=discord.OptionType.INTEGER,
                choices=[
                    discord.SlashCommandChoice(
                        name=f"Lvl. {i + 1}",
                        value=i + 1
                    ) for i in range(11)
                ],
                required=False
            )
        ]
    )
    async def chief_charm(self, ctx: discord.SlashContext, level: int, type: str, current: int = None):
        typeToTroop = {
            "keenness": "Lancer",
            "protection": "Infantry",
            "vision": "Marksman"
        }
        
        if typeToTroop[type] == "Lancer":
            color = 0x16a8e0
        elif typeToTroop[type] == "Infantry":
            color = 0x78e85c
        elif typeToTroop[type] == "Marksman":
            color = 0xebe12f
            
        stats = self.databaseChiefCharm[f"lvl{level}"]["stats"]
        
        url = f"https://raw.githubusercontent.com/zenpaiang/wos-database/refs/heads/master/chief_charm/{type}/lvl{level}.png"
        
        embed = discord.Embed(title=f"Lvl. {level} {type.capitalize()} Charm", color=color)
        
        embed.add_field("Stats", f"{typeToTroop[type]} Lethality: {stats}%\n{typeToTroop[type]} Health: {stats}%\n\n{self.databaseChiefCharm[f'lvl{level}']['power']} <:power:1316326705346121738>", inline=True)
        
        if current:
            dictKeys = list(self.databaseChiefCharm.keys())
            
            totalCostCurrent = {"charm_design": 0, "charm_guide": 0}
            
            for key in dictKeys[:dictKeys.index(f"lvl{current}") + 1]:
                costDict = self.databaseChiefCharm[key]["cost"]
                
                totalCostCurrent["charm_design"] += costDict["charm_design"]
                totalCostCurrent["charm_guide"] += costDict["charm_guide"]
                
            totalCostToGet = {"charm_design": 0, "charm_guide": 0}
            
            for key in dictKeys[:dictKeys.index(f"lvl{level}") + 1]:
                costDict = self.databaseChiefCharm[key]["cost"]
                
                totalCostToGet["charm_design"] += costDict["charm_design"]
                totalCostToGet["charm_guide"] += costDict["charm_guide"]

            totalCostToGet = {
                "charm_design": totalCostToGet["charm_design"] - totalCostCurrent["charm_design"], 
                "charm_guide": totalCostToGet["charm_guide"] - totalCostCurrent["charm_guide"]
            }
            
            embed.add_field(f"Materials Needed (from Lvl. {current} {type.capitalize()} Charm)", f"{totalCostToGet['charm_design']} <:charm_design:1316342556317057095>\n{totalCostToGet['charm_guide']} <:charm_guide:1316342536163426344>", inline=True)
        
        embed.set_thumbnail(url)
        embed.set_footer("powered by wos-database 💖")
        
        await ctx.send(embed=embed)
        
    @database_cmd.subcommand(
        sub_cmd_name="fire_crystals",
        sub_cmd_description="fire crystal amount requirements",
        options=[
            discord.SlashCommandOption(
                name="level",
                description="the fire crystal building level",
                type=discord.OptionType.INTEGER,
                required=True,
                choices=[
                    discord.SlashCommandChoice(
                        name=f"FC{i + 1}",
                        value=i + 1
                    ) for i in range(10)
                ]
            )
        ]
    )
    async def fire_crystals(self, ctx: discord.SlashContext, level: int):    
        embed_content = ""
        
        totalfc = 0
        totalrfc = 0
        
        for building in self.databaseFireCrystals[f"fc{level}"]:
            building_name = building.replace("_", " ").title()
            fc_value = self.databaseFireCrystals[f"fc{level}"][building]["fc"]
            rfc_value = self.databaseFireCrystals[f"fc{level}"][building]["rfc"]
            
            embed_content += f"**{building_name}:** {fc_value} <:fire_crystal:1318532416188710942>"
            
            if rfc_value > 0:
                embed_content += f" {rfc_value} <:refined_fire_crystal:1344884084429688934>"
                
            embed_content += "\n"
            
            totalfc += fc_value
            totalrfc += rfc_value
        
        embed_content += f"\n**Total:** {totalfc} <:fire_crystal:1318532416188710942>"
        
        if totalrfc > 0:
            embed_content += f" {totalrfc} <:refined_fire_crystal:1344884084429688934>"
        
        embed = discord.Embed(
            title=f"FC{level} Buildings",
            color=0xd53034,
            description=embed_content,
            thumbnail=discord.EmbedAttachment(
                url=f"https://raw.githubusercontent.com/zenpaiang/wos-database/refs/heads/master/fire_crystals/fc{level}.png",
            )
        )

        embed.set_footer("powered by wos-database 💖")
        
        await ctx.send(embed=embed)