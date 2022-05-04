import discord
import re 
from Tools.utils import getConfig, updateConfig, getGuildPrefix
from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class AllowSpamCog(commands.Cog, name="allow spam command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'allowspam', 
                        aliases= ["spam"],
                        usage="<#channel/ID> (False)",
                        description="Enable or disable the spam protection in a specific channel.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def allowspam(self, ctx, channel, remove=""):

        channel = re.findall(r'\d+', channel)[0] # Get only numbers from channel
        remove = remove.lower()

        prefix = await getGuildPrefix(self.bot, ctx)

        if remove != "false":
            try:
                channel  = int(channel)
                spamChannel = self.bot.get_channel(channel)

                data = getConfig(ctx.guild.id)

                if spamChannel.id in data["allowSpam"]:
                    embed = discord.Embed(title=self.bot.translate.msg(ctx.guild.id, "global", "ERROR"), description=self.bot.translate.msg(ctx.guild.id, "antiSpam", "CHANNEL_ALREADY_IGNORED_BY_ANTI_SPAM"), color=0xe00000) # Red
                    embed.set_footer(text=self.bot.translate.msg(ctx.guild.id, "global", "BOT_CREATOR"))
                    return await ctx.channel.send(embed=embed)

                data["allowSpam"].append(spamChannel.id)

                updateConfig(ctx.guild.id, data)
                embed = discord.Embed(title=self.bot.translate.msg(ctx.guild.id, "global", "SUCCESS"), description = self.bot.translate.msg(ctx.guild.id, "antiSpam", "CHANNEL_IGNORED_BY_ANTI_SPAM").format(spamChannel.id), color = 0x2fa737) # Green
                embed.set_footer(text=self.bot.translate.msg(ctx.guild.id, "global", "BOT_CREATOR"))
                await ctx.channel.send(embed = embed)

            except:
                embed = discord.Embed(title=self.bot.translate.msg(ctx.guild.id, "global", "ERROR"), description=self.bot.translate.msg(ctx.guild.id, "allowSpam", "INVALID_CHANNEL_ENABLE").format(prefix), color=0xe00000) # Red
                embed.set_footer(text=self.bot.translate.msg(ctx.guild.id, "global", "BOT_CREATOR"))
                return await ctx.channel.send(embed=embed)
        else:
            try:
                channel  = int(channel)
                spamChannel = self.bot.get_channel(channel)

                data = getConfig(ctx.guild.id)

                if spamChannel.id not in data["allowSpam"]:
                    embed = discord.Embed(title=self.bot.translate.msg(ctx.guild.id, "global", "ERROR"), description=self.bot.translate.msg(ctx.guild.id, "antiSpam", "ANTI_SPAM_ALREADY_DISABLED"), color=0xe00000) # Red
                    embed.set_footer(text=self.bot.translate.msg(ctx.guild.id, "global", "BOT_CREATOR"))
                    return await ctx.channel.send(embed=embed)

                data["allowSpam"].remove(spamChannel.id)
                

                updateConfig(ctx.guild.id, data)
                embed = discord.Embed(title=self.bot.translate.msg(ctx.guild.id, "global", "SUCCESS"), description = self.bot.translate.msg(ctx.guild.id, "antiSpam", "CHANNEL_NOT_IGNORED_BY_ANTI_SPAM").format(spamChannel.id), color = 0x2fa737) # Green
                embed.set_footer(text=self.bot.translate.msg(ctx.guild.id, "global", "BOT_CREATOR"))
                await ctx.channel.send(embed = embed)

            except:
                embed = discord.Embed(title=self.bot.translate.msg(ctx.guild.id, "global", "ERROR"), description=self.bot.translate.msg(ctx.guild.id, "antiSpam", "INVALID_CHANNEL_DISABLE").format(prefix), color=0xe00000) # Red
                embed.set_footer(text=self.bot.translate.msg(ctx.guild.id, "global", "BOT_CREATOR"))
                return await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(AllowSpamCog(bot))