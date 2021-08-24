import discord
import json
import re 
from Tools.utils import getConfig, updateConfig
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

        if remove != "false":
            try:
                channel  = int(channel)
                spamChannel = self.bot.get_channel(channel)

                data = getConfig(ctx.guild.id)

                if spamChannel.id in data["allowSpam"]:
                    embed = discord.Embed(title=f"**ERROR**", description=f"The channel where you want to allow to spam is already ignored by anti spam.", color=0xe00000) # Red
                    embed.set_footer(text="Bot Created by Darkempire#8245")
                    return await ctx.channel.send(embed=embed)

                data["allowSpam"].append(spamChannel.id)

                updateConfig(ctx.guild.id, data)
                embed = discord.Embed(title = f"**SUCCESS**", description = f"The <#{spamChannel.id}> channel is ignored by the anti spam.", color = 0x2fa737) # Green
                embed.set_footer(text="Bot Created by Darkempire#8245")
                await ctx.channel.send(embed = embed)

            except:
                embed = discord.Embed(title=f"**ERROR**", description=f"The channel where you want to allow to spam must be a text channel\nFollow the example : ``{self.bot.command_prefix}allowspam <#channel>``", color=0xe00000) # Red
                embed.set_footer(text="Bot Created by Darkempire#8245")
                return await ctx.channel.send(embed=embed)
        else:
            try:
                channel  = int(channel)
                spamChannel = self.bot.get_channel(channel)

                data = getConfig(ctx.guild.id)

                if spamChannel.id not in data["allowSpam"]:
                    embed = discord.Embed(title=f"**ERROR**", description=f"The channel where you want to disable the spam is already disabled.", color=0xe00000) # Red
                    embed.set_footer(text="Bot Created by Darkempire#8245")
                    return await ctx.channel.send(embed=embed)

                data["allowSpam"].remove(spamChannel.id)
                

                updateConfig(ctx.guild.id, data)
                embed = discord.Embed(title = f"**SUCCESS**", description = f"The <#{spamChannel.id}> channel is not ignored by the anti spam.", color = 0x2fa737) # Green
                embed.set_footer(text="Bot Created by Darkempire#8245")
                await ctx.channel.send(embed = embed)

            except:
                embed = discord.Embed(title=f"**ERROR**", description=f"The channel where you want to disable the spam must be a channel\nFollow the example : ``{self.bot.command_prefix}allowspam <#channel> remove``", color=0xe00000) # Red
                embed.set_footer(text="Bot Created by Darkempire#8245")
                return await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(AllowSpamCog(bot))