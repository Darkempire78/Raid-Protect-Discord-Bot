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
                embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "moderation", "YOU_HAVE_BEEN_KICKED").format(guild.name), description = self.bot.translate.msg(ctx.guild.id, "moderation", "KICK_REASON").format(reason), color = 0xff0000)
                await memberToKick.send(embed = embed)
                
                await memberToKick.kick()
                
                if reason:
                    await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "HAS_BEEN_KICKED_WHITH_REASON").format(memberToKick, reason))
                else:
                    await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "HAS_BEEN_KICKED_WHITHOUT_REASON").format(memberToKick))
            
            except Exception as error:
                return await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "global", "ERROR_OCCURED").format(error))

        else:
            await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "MEMBER_NOT_FOUND"))
    

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
                embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "moderation", "YOU_HAVE_BEEN_BANNED"), description = self.bot.translate.msg(ctx.guild.id, "moderation", "BAN_REASON").format(reason), color = 0xff0000)
                await memberToBan.send(embed = embed)
                
                await memberToBan.ban()

                if reason:
                    await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "HAS_BEEN_BANNED_WHITH_REASON").format(memberToBan, reason))
                else:
                    await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "HAS_BEEN_BANNED_WHITHOUT_REASON").format(memberToBan))
            
            except Exception as error:
                return await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "global", "ERROR_OCCURED").format(error))
            
        else:
            await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "MEMBER_NOT_FOUND"))


def setup(bot:commands.Bot):
    bot.add_cog(ModerationCog(bot))