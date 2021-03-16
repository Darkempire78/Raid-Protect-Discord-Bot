import discord
import asyncio
import json

from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions

# ------------------------ COGS ------------------------ #


class MinAccountAgeCog(commands.Cog, name="change min account age command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #

    @commands.command(name='minaccountage',
                      aliases=["minage", "agarequired", "age"],
                      usage="<数字（1時間単位）/false>",
                      description="アカウントを作成してどのぐらい経った人が参加できるかの制限を更新または無効にします。")
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def minaccountage(self, ctx, accountAge):

        accountAge = accountAge.lower()

        if accountAge == "false":
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["minAccountDate"] = False
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            with open("configuration.json", "w") as config:
                config.write(newdata)

            embed = discord.Embed(
                title=f"**無効にしました**", description=f"アカウントを作成した時間による制限は無効になりました", color=0x2fa737)  # Green
            await ctx.channel.send(embed=embed)
        else:
            try:
                accountAge = int(accountAge)
                # hour to second
                accountAge *= 3600

                # Edit configuration.json
                with open("configuration.json", "r") as config:
                    data = json.load(config)
                    # Add modifications
                    data["minAccountDate"] = accountAge
                    newdata = json.dumps(data, indent=4, ensure_ascii=False)

                with open("configuration.json", "w") as config:
                    config.write(newdata)

                embed = discord.Embed(
                    title=f"**更新しました**", description=f"アカウントを作成した時間による制限を更新しました", color=0x2fa737)  # Green
                await ctx.channel.send(embed=embed)

            except:
                embed = discord.Embed(
                    title=f"**エラー**", description=f"数字を指定してください (デフォルトでは24時間です)\n例 : ``{self.bot.command_prefix}minaccountage <数字 (1時間単位)>``", color=0xe00000)  # Red
                embed.set_footer(text="Bot Created by Darkempire#8245")
                return await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.add_cog(MinAccountAgeCog(bot))
