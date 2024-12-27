import interactions as discord
import hashlib
import certifi
import aiohttp
import time
import ssl

class Utils(discord.Extension):
    @discord.slash_command(
        name="user",
        description="user-related commands",
        sub_cmd_name="info",
        sub_cmd_description="get user information",
        options=[
            discord.SlashCommandOption(
                name="id",
                description="the user's in game id",
                type=discord.OptionType.INTEGER,
                required=True                
            )
        ]
    )
    async def user_info(self, ctx: discord.SlashContext, id: int):
        await ctx.defer()
        
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl.create_default_context(cafile=certifi.where())))
        
        timens = time.time_ns()
        
        login_resp = await session.post(
            url="https://wos-giftcode-api.centurygame.com/api/player",
            data={
                "fid": id,
                "time": timens,
                "sign": hashlib.md5(f"fid={id}&time={timens}tB87#kPtkxqOS2".encode("utf-8")).hexdigest()
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            timeout=30
        )
        
        await session.close()
        
        try:
            login_result = await login_resp.json()
            
            if login_result["code"] != 0:
                raise Exception()
            
            login_result = login_result["data"]
        except Exception as _:
            await ctx.send("error: failed to fetch user data")
            return
        
        def furnace_content_from_int(fl: int) -> str:
            if fl <= 30:
                return str(fl)

            base_level = (fl - 31) // 5 + 1
            level = f"FC{base_level}"
        
            remainder = (fl - 30) % 5
            
            EMOJIS = {
                "FC1": 1321753229570080778,
                "FC2": 1321753236465520691,
                "FC3": 1321753243285590047,
                "FC4": 1321753252789882921,
                "FC5": 1321753263611187290,
                "FC6": 1321753271882219562,
                "FC7": 1321753280388403251,
                "FC8": 1321753288399650888,
                "FC9": 1321753295244492831,
                "FC10": 1321753302165098527
            }
            
            if remainder > 0:
                prev_level = "30" if base_level == 1 else f"FC{base_level - 1}"
                
                return f"30 - {remainder}/5 to <:{level}:{EMOJIS[level]}>" if base_level == 1 else f"<:{prev_level}:{EMOJIS[prev_level]}> - {remainder}/5 to <:{level}:{EMOJIS[level]}>"
            
            return f"<:{level}:{EMOJIS[level]}>"
        
        embed = discord.Embed(
            title=f"#{login_result['kid']} {login_result['nickname']}",
            description=f"**furnace level:** {furnace_content_from_int(login_result['stove_lv'])}\n**user id:** `{id}`\n\n[profile picture]({login_result['avatar_image']})",
            color=0x5865f2
        )
        
        embed.set_thumbnail(login_result["avatar_image"])
        
        await ctx.send(embed=embed)