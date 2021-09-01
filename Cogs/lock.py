import discord
import re 

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class LockCog(commands.Cog, name="lock command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'lock',
                        usage="(#channel/ID)",
                        description="Lock the channel.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def lock (self, ctx, channel=None):

        # Get channel
        if channel:
            channel = re.findall(r'\d+', channel) # Get only numbers from channel
            channel = self.bot.get_channel(int(channel[0]))
        else:
            channel = ctx.channel

        if channel:
            await channel.edit(name=f"🔒-{channel.name}")

            perms = channel.overwrites_for(ctx.guild.default_role)
            perms.send_messages=False
            await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
            
            embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "lock", "LOCKED_WITH_SUCCESS").format(channel.name), description = f"", color = 0x2fa737) # Green
            await ctx.channel.send(embed = embed)
        else:
            await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "lock", "CHANNEL_NOT_FOUND"))


# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(LockCog(bot))