import discord

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'help')
    async def help (self, ctx):
        embed = discord.Embed(title=f"__**Help page of {self.bot.user.name}**__", description="[**GitHub**]()", color=0xdeaa0c)
        embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
        embed.add_field(name="__COMMANDS :__", value=f"**{self.bot.command_prefix}setup <on/off> :** Set up the captcha protection.\n**{self.bot.command_prefix}settings :** Display the list of settings.\n**{self.bot.command_prefix}giveroleaftercaptcha <role ID/off> :** Give a role after that the user passed the captcha.\n**{self.bot.command_prefix}minaccountage <number (hours)> :** set a minimum age to join the server (24 hours by default).\n**{self.bot.command_prefix}antiSpam <true/false> :** Enable or disable the spam protection.", inline=False)
        embed.set_footer(text="Bot Created by Darkempire#8245")
        await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))