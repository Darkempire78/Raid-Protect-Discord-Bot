import discord
import re 

from random import randint 

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class UserInfosCog(commands.Cog, name="user infos command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'userinfos', aliases=["ui", "userinfo", "info", "infos"])
    async def userinfos (self, ctx, member):

        # Get member
        member = re.findall(r'\d+', member) # Get only numbers from member
        member = self.bot.get_user(int(member[0]))

        if member != None:
            embed = discord.Embed(title=f"__**{member.name} informations :**__", description="[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)", color=randint(0, 0xffffff))
            embed.set_thumbnail(url=f'{member.avatar_url}')
            embed.add_field(name="**Member ID :**", value=f"{member.id}", inline=True)
            embed.add_field(name="**Account creation :**", value=f"{member.created_at.year}-{member.created_at.month}-{member.created_at.day} {member.created_at.hour}:{member.created_at.minute}:{member.created_at.second}", inline=True)
            for guildMember in ctx.guild.members:
                if guildMember == member:
                    embed.add_field(name="**Joined at :**", value=f"{guildMember.joined_at.year}-{guildMember.joined_at.month}-{guildMember.joined_at.day} {guildMember.joined_at.hour}:{guildMember.joined_at.minute}:{guildMember.joined_at.second}", inline=True)
            embed.set_footer(text="Bot Created by Darkempire#8245")
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("Member not found!")

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(UserInfosCog(bot))