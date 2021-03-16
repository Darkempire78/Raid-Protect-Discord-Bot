import discord
import asyncio
import json
import re

from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions

# ------------------------ COGS ------------------------ #


class AllowSpamCog(commands.Cog, name="スパム許可コマンド"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #

    @commands.command(name='allowspam',
                      aliases=["spam"],
                      usage="<#channel/ID> (remove)",
                      description="指定したチャンネルのスパム許可・拒否を設定します。")
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def allowspam(self, ctx, channel, remove="False"):

        channel = re.findall(r'\d+', channel)  # Get only numbers from channel

        if remove == "False":
            try:
                channel = int(channel)
                spamChannel = self.bot.get_channel(channel)

                # Edit configuration.json
                with open("configuration.json", "r") as config:
                    data = json.load(config)

                if spamChannel.id in data["allowSpam"]:
                    embed = discord.Embed(
                        title=f"**エラー**", description=f"指定したチャンネルでは既にスパムが許可されています。", color=0xe00000)  # Red
                    embed.set_footer(text="Bot Created by Darkempire#8245")
                    return await ctx.channel.send(embed=embed)

                data["allowSpam"].append(spamChannel.id)
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

                with open("configuration.json", "w") as config:
                    config.write(newdata)
                embed = discord.Embed(
                    title=f"**成功**", description=f"<#{spamChannel.id}> でのスパムを許可する設定にしました。", color=0x2fa737)  # Green
                embed.set_footer(text="Bot Created by Darkempire#8245")
                await ctx.channel.send(embed=embed)

            except:
                embed = discord.Embed(
                    title=f"**エラー**", description=f"正しいチャンネルを指定してください。\n例 : ``{self.bot.command_prefix}allowspam <#channel>``", color=0xe00000)  # Red
                embed.set_footer(text="Bot Created by Darkempire#8245")
                return await ctx.channel.send(embed=embed)
        else:
            try:
                channel = int(channel)
                spamChannel = self.bot.get_channel(channel)

                # Edit configuration.json
                with open("configuration.json", "r") as config:
                    data = json.load(config)

                if spamChannel.id not in data["allowSpam"]:
                    embed = discord.Embed(
                        title=f"**エラー**", description=f"指定したチャンネルでは既にスパムが禁止されています。", color=0xe00000)  # Red
                    embed.set_footer(text="Bot Created by Darkempire#8245")
                    return await ctx.channel.send(embed=embed)

                data["allowSpam"].remove(spamChannel.id)
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

                with open("configuration.json", "w") as config:
                    config.write(newdata)
                embed = discord.Embed(
                    title=f"**成功**", description=f"<#{spamChannel.id}> でのスパムを禁止する設定にしました。", color=0x2fa737)  # Green
                embed.set_footer(text="Bot Created by Darkempire#8245")
                await ctx.channel.send(embed=embed)

            except:
                embed = discord.Embed(
                    title=f"**エラー**", description=f"正しいチャンネルを設定してください。\n例 : ``{self.bot.command_prefix}allowspam <#channel> remove``", color=0xe00000)  # Red
                embed.set_footer(text="Bot Created by Darkempire#8245")
                return await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.add_cog(AllowSpamCog(bot))
