import re
import asyncio
import discord
from discord.ext import commands
from discord.utils import get


class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="kick",
                      usage="<@user/ID>",
                      description="Kick a user.")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def kick(self, ctx: commands.Context, member, *reason):

        # Get the user
        member = re.findall(r'\d+', member)
        guild = ctx.guild
        memberToKick = get(guild.members, id=int(member[0]))

        if memberToKick:
            try:
                reason = " ".join(reason)
                embed = discord.Embed(title=f"**YOU HAVE BEEN KICKED FROM {guild.name}**",
                                      description=f"Reason : `{reason}`", color=0xff0000)
                await memberToKick.send(embed=embed)

                await memberToKick.kick()

                if reason:
                    await ctx.channel.send(f"{memberToKick} has been kicked with the reason : `{reason}` 🔨")
                else:
                    await ctx.channel.send(f"{memberToKick} has been kicked without reason 🔨")

            except Exception as error:
                return await ctx.channel.send(f"An error was occcured : `{error}`")

        else:
            await ctx.channel.send("Member not found!")

    @commands.command(name="ban",
                      usage="<@user/ID>",
                      description="Ban a user.")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ban(self, ctx: commands.Context, member, **reason):

        # Get the user
        member = re.findall(r'\d+', member)
        guild = ctx.guild
        memberToBan = get(guild.members, id=int(member[0]))

        if memberToBan:
            try:
                reason = " ".join(reason)
                embed = discord.Embed(title=f"**YOU HAVE BEEN BANNED FROM {guild.name}**",
                                      description=f"Reason : `{reason}`", color=0xff0000)
                await memberToBan.send(embed=embed)

                await memberToBan.ban()

                if reason:
                    await ctx.channel.send(f"{memberToBan} has been banned for: `{reason}` 🔨")
                else:
                    await ctx.channel.send(f"{memberToBan} has been banned for no reason 🔨")

            except Exception as error:
                return await ctx.channel.send(f"An error was occcured : `{error}`")

        else:
            await ctx.channel.send("Member not found!")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, time):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        tempmute = int(time[0]) * time_convert[time[-1]]
        await ctx.message.delete()
        await member.add_roles(muted_role)
        embed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} muted successfuly**",
                              color=discord.Color.green())
        await ctx.send(embed=embed, delete_after=1)
        await asyncio.sleep(tempmute)
        await member.remove_roles(muted_role)

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.message.delete()

    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await ctx.message.delete()
        await member.remove_roles(mutedRole)


def setup(bot: commands.Bot):
    bot.add_cog(ModerationCog(bot))
