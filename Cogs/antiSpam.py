import discord
import json
from discord.ext import commands
from Tools.utils import getConfig, updateConfig

# ------------------------ COGS ------------------------ #  

class AntiSpamCog(commands.Cog, name="change setting from anti spam command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'antispam', 
                        usage="<true/false>",
                        description="Enable or disable the spam protection.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def antispam(self, ctx, antiSpam):

        antiSpam = antiSpam.lower()

        if antiSpam == "true":
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["antiSpam"] = True
            

            embed = discord.Embed(title = f"**ANTI SPAM WAS ENABLED**", description = f"The anti spam was enabled.", color = 0x2fa737) # Green
        else:
            config = getConfig(ctx.guild.id)
            data = json.load(config)
            # Add modifications
            data["antiSpam"] = False
            

            embed = discord.Embed(title = f"**ANTI SPAM WAS DISABLED**", description = f"The anti spam was disabled.", color = 0xe00000) # Red
        
        await ctx.channel.send(embed = embed)
        
        updateConfig(ctx.guild.id, data)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(AntiSpamCog(bot))