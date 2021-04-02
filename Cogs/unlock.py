import discord
import re 

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class UnlockCog(commands.Cog, name="unlock command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'unlock',
                        usage="<#channel/ID>",
                        description="Unlock the channel.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def unlock (self, ctx, channel):

        # Get channel
        channel = re.findall(r'\d+', channel) # Get only numbers from channel
        channel = self.bot.get_channel(int(channel[0]))

        if channel:
            await channel.edit(name=channel.name.replace("🔒-", "", 1))
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            embed = discord.Embed(title = f"#{channel.name} unlocked with success!", description = f"", color = 0x2fa737) # Green
            await ctx.channel.send(embed = embed)
        else:
            await ctx.channel.send("Channel not found!")

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(UnlockCog(bot))