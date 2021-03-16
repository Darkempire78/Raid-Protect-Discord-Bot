import discord
import asyncio
import json

from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions

# ------------------------ COGS ------------------------ #


class AntiSpamCog(commands.Cog, name="スパム保護の設定をします"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #

    @commands.command(name='antispam',
                      usage="<true/false>",
                      description="スパム保護の有効・無効を設定します")
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def antispam(self, ctx, antiSpam):

        antiSpam = antiSpam.lower()

        if antiSpam == "true":
            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["antiSpam"] = True
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(
                title=f"**保護が有効になりました**", description=f"スパム保護をする設定にしました。", color=0x2fa737)  # Green
        else:
            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["antiSpam"] = False
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(
                title=f"**保護が無効になりました**", description=f"スパム保護をしない設定にしました。", color=0xe00000)  # Red

        await ctx.channel.send(embed=embed)

        with open("configuration.json", "w") as config:
            config.write(newdata)

# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.add_cog(AntiSpamCog(bot))
