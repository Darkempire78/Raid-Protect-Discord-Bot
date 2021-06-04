import discord
from discord.ext import commands
from discord.utils import get

import re 


class ModerationCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "kick",
                    usage="<@user/ID>",
                    description = "Kick a user.")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def kick(self, ctx:commands.Context, member, *reason):

        # Get the user
        member = re.findall(r'\d+', member) 
        guild = ctx.guild
        memberToKick = get(guild.members, id=int(member[0]))

        if memberToKick:
            try:
                reason = " ".join(reason)
                embed = discord.Embed(title = f"**YOU HAVE BEEN KICKED FROM {guild.name}**", description = f"Reason : `{reason}`", color = 0xff0000)
                await memberToKick.send(embed = embed)
                
                await memberToKick.kick()
                
                if reason:
                    await ctx.channel.send(f"{memberToKick} has been kicked with the reason : `{reason}` 🔨")
                else:
                    await ctx.channel.send(f"{memberToKick} has been kicked without reason 🔨")
            
            except Exception as error:
                return await ctx.channel.send(f"An error was occcured : `{error}`")

        else:
            await ctx.channel.send("Member not found!")
    

    @commands.command(name = "ban",
                    usage="<@user/ID>",
                    description = "Ban a user.")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ban(self, ctx:commands.Context, member, **reason):

        # Get the user
        member = re.findall(r'\d+', member) 
        guild = ctx.guild
        memberToBan = get(guild.members, id=int(member[0]))

        if memberToBan:
            try:
                reason = " ".join(reason)
                embed = discord.Embed(title = f"**YOU HAVE BEEN BANNED FROM {guild.name}**", description = f"Reason : `{reason}`", color = 0xff0000)
                await memberToBan.send(embed = embed)
                
                await memberToBan.ban()

                if reason:
                    await ctx.channel.send(f"{memberToBan} has been banned with the reason : `{reason}` 🔨")
                else:
                    await ctx.channel.send(f"{memberToBan} has been banned without reason 🔨")
            
            except Exception as error:
                return await ctx.channel.send(f"An error was occcured : `{error}`")
            
        else:
            await ctx.channel.send("Member not found!")


def setup(bot:commands.Bot):
    bot.add_cog(ModerationCog(bot))