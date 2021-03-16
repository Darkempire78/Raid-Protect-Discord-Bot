import discord
import re

from discord.ext import commands

# ------------------------ COGS ------------------------ #


class LockCog(commands.Cog, name="lock command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #

    @commands.command(name='lock',
                      usage="<#channel/ID>",
                      description="チャンネルをロックします")
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def lock(self, ctx, channel):

        # Get channel
        channel = re.findall(r'\d+', channel)  # Get only numbers from channel
        channel = self.bot.get_channel(int(channel[0]))

        if channel is None:
            await channel.edit(name=f"🔒-{channel.name}")
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed = discord.Embed(
                title=f"#{channel.name} をロックしました", description=f"", color=0x2fa737)  # Green
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("チャンネルが見つかりません！")

# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.add_cog(LockCog(bot))
