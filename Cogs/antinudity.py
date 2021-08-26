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
            

            embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "antinudity", "ANTI_NUDITY_ENABLED"), description = self.bot.translate.msg(ctx.guild.id, "antinudity", "ANTI_NUDITY_ENABLED_DESCRIPTION"), color = 0x2fa737) # Green
        else:
            data = getConfig(ctx.guild.id)
            # Add modifications
            data["antiNudity"] = False
            

            embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "antinudity", "ANTI_NUDITY_DISABLED"), description = self.bot.translate.msg(ctx.guild.id, "antinudity", "ANTI_NUDITY_DISABLED_DESCRIPTION"), color = 0xe00000) # Red
        
        await ctx.channel.send(embed = embed)
        
        updateConfig(ctx.guild.id, data)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(AntiNudityCog(bot))