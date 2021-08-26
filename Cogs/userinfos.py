import discord
import re 

from random import randint 

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class UserInfosCog(commands.Cog, name="user infos command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'userinfos', 
                        aliases=["ui", "userinfo", "info", "infos"],
                        usage="<@user/ID>",
                        description="Displays data from user.")
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def userinfos (self, ctx, member):

        # Get member
        member = re.findall(r'\d+', member) # Get only numbers from member
        member = self.bot.get_user(int(member[0]))

        if member is not None:
            embed = discord.Embed(title=self.bot.translate.msg(ctx.guild.id, "userinfos", "USER_INFORMATIONS").format(member.name), description="[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)", color=randint(0, 0xffffff))
            embed.set_thumbnail(url=f'{member.avatar_url}')
            embed.add_field(name=self.bot.translate.msg(ctx.guild.id, "userinfos", "MEMBER_ID"), value=f"{member.id}", inline=True)
            embed.add_field(name=self.bot.translate.msg(ctx.guild.id, "userinfos", "ACCOUNT_CREATION"), value=f"{member.created_at.year}-{member.created_at.month}-{member.created_at.day} {member.created_at.hour}:{member.created_at.minute}:{member.created_at.second}", inline=True)
            for guildMember in ctx.guild.members:
                if guildMember == member:
                    embed.add_field(name=self.bot.translate.msg(ctx.guild.id, "userinfos", "JOINED_AT"), value=f"{guildMember.joined_at.year}-{guildMember.joined_at.month}-{guildMember.joined_at.day} {guildMember.joined_at.hour}:{guildMember.joined_at.minute}:{guildMember.joined_at.second}", inline=True)
            embed.set_footer(text=self.bot.translate.msg(ctx.guild.id, "global", "BOT_CREATOR"))
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "userinfos", "MEMBER_NOT_FOUND"))

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(UserInfosCog(bot))