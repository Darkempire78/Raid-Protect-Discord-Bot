import discord
import json
from Tools.utils import getConfig, updateConfig
from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class AntiNudityCog(commands.Cog, name="change setting from anti nudity command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'antinudity', 
                        aliases= ["nudity", "porn"],
                        usage="<true/false>",
                        description="Enable or disable the nudity image protection.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def antinudity(self, ctx, antiNudity):

        antiNudity = antiNudity.lower()

        if antiNudity == "true":
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["antiNudity"] = True
            newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**ANTI NUDITY WAS ENABLED**", description = f"The anti nudity was enabled.", color = 0x2fa737) # Green
        else:
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["antiNudity"] = False
            newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**ANTI NUDITY WAS DISABLED**", description = f"The anti nudity was disabled.", color = 0xe00000) # Red
        
        await ctx.channel.send(embed = embed)
        
        updateConfig(ctx.guild.id, newdata)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(AntiNudityCog(bot))