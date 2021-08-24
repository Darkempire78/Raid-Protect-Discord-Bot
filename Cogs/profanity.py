import discord
import json
from discord.ext import commands
from Tools.utils import getConfig, updateConfig

# ------------------------ COGS ------------------------ #  

class AntiProfanityCog(commands.Cog, name="change setting from anti nudity command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'antiprofanity', 
                        aliases= ["profanity"],
                        usage="<true/false>",
                        description="Enable or disable the anti profanity.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def antiprofanity(self, ctx, antiProfanity):

        antiProfanity = antiProfanity.lower()

        if antiProfanity == "true":
            data = getConfig()
            data["antiProfanity"] = True
            newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**ANTI PROFANITY WAS ENABLED**", description = f"The anti profanity was enabled.", color = 0x2fa737) # Green
        else:
            data = getConfig()
            data["antiProfanity"] = False
            newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**ANTI PROFANITY WAS DISABLED**", description = f"The anti profanity was disabled.", color = 0xe00000) # Red
        
        await ctx.channel.send(embed = embed)
        
        updateConfig(newdata)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(AntiProfanityCog(bot))