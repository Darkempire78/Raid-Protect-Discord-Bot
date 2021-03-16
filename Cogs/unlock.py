import discord
import re

from discord.ext import commands


# ------------------------ COGS ------------------------ #

class UnlockCog(commands.Cog, name="アンロックコマンド"):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------------------------------------ #

    @commands.command(name='unlock',
                      usage="<#channel/ID>",
                      description="チャンネルをアンロックします。")
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def unlock(self, ctx, channel):

        # Get channel
        channel_ids = re.findall(r'\d+', channel)  # Get only numbers from channel
        channel = self.bot.get_channel(int(channel_ids[0]))

        if channel is not None:
            await channel.edit(name=channel.name.replace("🔒-", "", 1))
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            embed = discord.Embed(title=f"#{channel.name}を正常にアンロックしました！", description=f"",
                                  color=0x2fa737)  # Green
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("チャンネルが見つかりません。")


# ------------------------ BOT ------------------------ #

def setup(bot):
    bot.add_cog(UnlockCog(bot))
