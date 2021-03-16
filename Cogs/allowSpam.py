import discord
import json
import re

from discord.ext import commands
from discord.ext.commands import has_permissions


# ------------------------ COGS ------------------------ #


class AllowSpamCog(commands.Cog, name="スパム許可コマンド"):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------------------------------------ #

    # noinspection PyBroadException
    @commands.command(name='allowspam',
                      aliases=["spam"],
                      usage="<#channel/ID> (remove)",
                      description="指定したチャンネルのスパム許可・拒否を設定します。")
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def allow_spam(self, ctx, channel_id, remove="False"):

        channel_list = re.findall(r'\d+', channel_id)  # Get only numbers from channel
        channel_id = channel_list[0]

        if remove == "False":
            try:
                channel_id = int(channel_id)
                spam_channel = self.bot.get_channel(channel_id)

                # Edit configuration.json
                with open("configuration.json", "r") as config:
                    data = json.load(config)

                if spam_channel.id in data["allowSpam"]:
                    embed = discord.Embed(
                        title=f"**エラー**", description=f"指定したチャンネルでは既にスパムが許可されています。", color=0xe00000)  # Red
                    embed.set_footer(text="Bot Created by Darkempire#8245")
                    return await ctx.channel.send(embed=embed)

                data["allowSpam"].append(spam_channel.id)
                new_data = json.dumps(data, indent=4, ensure_ascii=False)

                with open("configuration.json", "w") as config:
                    config.write(new_data)
                embed = discord.Embed(
                    title=f"**成功**", description=f"<#{spam_channel.id}> でのスパムを許可する設定にしました。", color=0x2fa737)  # Green
                embed.set_footer(text="Bot Created by Darkempire#8245")
                await ctx.channel.send(embed=embed)

            except Exception:
                embed = discord.Embed(
                    title=f"**エラー**",
                    description=f"正しいチャンネルを指定してください。\n例 : ``{self.bot.command_prefix}allowspam <#channel>``",
                    color=0xe00000)  # Red
                embed.set_footer(text="Bot Created by Darkempire#8245")
                return await ctx.channel.send(embed=embed)
        else:
            try:
                channel_id = int(channel_id)
                spam_channel = self.bot.get_channel(channel_id)

                # Edit configuration.json
                with open("configuration.json", "r") as config:
                    data = json.load(config)

                if spam_channel.id not in data["allowSpam"]:
                    embed = discord.Embed(
                        title=f"**エラー**", description=f"指定したチャンネルでは既にスパムが禁止されています。", color=0xe00000)  # Red
                    embed.set_footer(text="Bot Created by Darkempire#8245")
                    return await ctx.channel.send(embed=embed)

                data["allowSpam"].remove(spam_channel.id)
                new_data = json.dumps(data, indent=4, ensure_ascii=False)

                with open("configuration.json", "w") as config:
                    config.write(new_data)
                embed = discord.Embed(
                    title=f"**成功**", description=f"<#{spam_channel.id}> でのスパムを禁止する設定にしました。", color=0x2fa737)  # Green
                embed.set_footer(text="Bot Created by Darkempire#8245")
                await ctx.channel.send(embed=embed)

            except Exception:
                embed = discord.Embed(
                    title=f"**エラー**",
                    description=f"正しいチャンネルを設定してください。\n例 : ``{self.bot.command_prefix}allowspam <#channel> remove``",
                    color=0xe00000)  # Red
                embed.set_footer(text="Bot Created by Darkempire#8245")
                return await ctx.channel.send(embed=embed)


# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.add_cog(AllowSpamCog(bot))
