import discord
import re

from random import randint

from discord.ext import commands


# ------------------------ COGS ------------------------ #

class UserInfosCog(commands.Cog, name="ユーザー情報コマンド"):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------------------------------------ #

    @commands.command(name='userinfos',
                      aliases=["ui", "userinfo", "info", "infos"],
                      usage="<@user/ID>",
                      description="ユーザーのデータを表示します。")
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def user_infos(self, ctx, member):

        # Get member
        member_ids = re.findall(r'\d+', member)  # Get only numbers from member
        member = self.bot.get_user(int(member_ids[0]))

        if member is not None:
            embed = discord.Embed(title=f"__**{member.name} ユーザー情報 :**__",
                                  description="[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)",
                                  color=randint(0, 0xffffff))
            embed.set_thumbnail(url=f'{member.avatar_url}')
            embed.add_field(name="**Id :**", value=f"{member.id}", inline=True)
            embed.add_field(name="**アカウント作成日時 :**",
                            value=f"{member.created_at.year}-{member.created_at.month}-{member.created_at.day} {member.created_at.hour}:{member.created_at.minute}:{member.created_at.second}",
                            inline=True)
            for guildMember in ctx.guild.members:
                if guildMember == member:
                    embed.add_field(name="**サーバー参加日時 :**",
                                    value=f"{guildMember.joined_at.year}-{guildMember.joined_at.month}-{guildMember.joined_at.day} {guildMember.joined_at.hour}:{guildMember.joined_at.minute}:{guildMember.joined_at.second}",
                                    inline=True)
            embed.set_footer(text="Bot Created by Darkempire#8245")
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("メンバーが見つかりません。")


# ------------------------ BOT ------------------------ #

def setup(bot):
    bot.add_cog(UserInfosCog(bot))
