import json

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


# ------------------------ COGS ------------------------ #


class MinAccountAgeCog(commands.Cog, name="change min account age command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #

    # noinspection PyBroadException
    @commands.command(name='minaccountage',
                      aliases=["minage", "agarequired", "age"],
                      usage="<数字（1時間単位）/false>",
                      description="アカウントを作成してどのぐらい経った人が参加できるかの制限を更新または無効にします。")
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def min_account_age(self, ctx, account_age):

        account_age = account_age.lower()

        if account_age == "false":
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["minAccountDate"] = False
                new_data = json.dumps(data, indent=4, ensure_ascii=False)

            with open("configuration.json", "w") as config:
                config.write(new_data)

            embed = discord.Embed(
                title=f"**無効にしました**", description=f"アカウントを作成した時間による制限は無効になりました", color=0x2fa737)  # Green
            await ctx.channel.send(embed=embed)
        else:
            try:
                account_age = int(account_age)
                # hour to second
                account_age *= 3600

                # Edit configuration.json
                with open("configuration.json", "r") as config:
                    data = json.load(config)
                    # Add modifications
                    data["minAccountDate"] = account_age
                    new_data = json.dumps(data, indent=4, ensure_ascii=False)

                with open("configuration.json", "w") as config:
                    config.write(new_data)

                embed = discord.Embed(
                    title=f"**更新しました**", description=f"アカウントを作成した時間による制限を更新しました", color=0x2fa737)  # Green
                await ctx.channel.send(embed=embed)

            except Exception:
                embed = discord.Embed(
                    title=f"**エラー**", description=f"数字を指定してください (デフォルトでは24時間です)\n"
                                                  f"例 : ``{self.bot.command_prefix}minaccountage <数字 (1時間単位)>``",
                    color=0xe00000)  # Red
                embed.set_footer(text="Bot Created by Darkempire#8245")
                return await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.add_cog(MinAccountAgeCog(bot))
