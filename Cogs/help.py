import discord
from discord.ext import commands
from Tools.utils import getGuildPrefix

# ------------------------ COGS ------------------------ #  

class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'help',
                        usage="(commandName)",
                        description = "Display the help message.")
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def help(self, ctx, commandName=None):

        commandName2 = None
        stop = False

        if commandName is not None:
            for i in self.bot.commands:
                if i.name == commandName.lower():
                    commandName2 = i
                    break 
                else:
                    for j in i.aliases:
                        if j == commandName.lower():
                            commandName2 = i
                            stop = True
                            break
                if stop:
                    break 

            if commandName2 is None:
                await ctx.channel.send("No command found!")   
            else:
                embed = discord.Embed(title=f"**{commandName2.name.upper()} COMMAND :**", description="[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)", color=0xdeaa0c)
                embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
                embed.add_field(name=f"**NAME :**", value=f"{commandName2.name}", inline=False)
                aliases = ""
                if len(commandName2.aliases) > 0:
                    for aliase in commandName2.aliases:
                        aliases = aliase
                else:
                    commandName2.aliases = None
                    aliases = None
                embed.add_field(name=f"**ALIASES :**", value=f"{aliases}", inline=False)
                if commandName2.usage is None:
                    commandName2.usage = ""
                    
                prefix = await getGuildPrefix(self.bot, ctx)
                embed.add_field(name=f"**USAGE :**", value=f"{prefix}{commandName2.name} {commandName2.usage}", inline=False)
                embed.add_field(name=f"**DESCRIPTION :**", value=f"{commandName2.description}", inline=False)
                embed.set_footer(text="Bot Created by Darkempire#8245")
                await ctx.channel.send(embed=embed)
        else:
            prefix = await getGuildPrefix(self.bot, ctx)
            embed = discord.Embed(title=f"__**Help page of {self.bot.user.name.upper()}**__", description="[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)\n\n**{prefix}help (command) :**Display the help list or the help data for a specific command.", color=0xdeaa0c)
            embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
            embed.add_field(name=f"__ADMIN :__", value=f"**{prefix}setup <on/off> :** Set up the captcha protection.\n**{prefix}settings :** Display the list of settings.\n**{prefix}giveroleaftercaptcha <role ID/off> :** Give a role after that the user passed the captcha.\n**{prefix}minaccountage <number (hours)> :** set a minimum age to join the server (24 hours by default).\n**{prefix}antinudity <true/false> :** Enable or disable the nudity image protection.\n**{prefix}antiprofanity <true/false> :** Enable or disable the profanity protection.\n**{prefix}antispam <true/false> :** Enable or disable the spam protection.\n**{prefix}allowspam <#channel> (remove) :** Enable or disable the spam protection in a specific channel.\n**{prefix}lock | unlock <#channel/ID> :** Lock/Unlock a channel.\n\n**{prefix}kick <@user/ID> :** Kick the user.\n**{prefix}ban <@user/ID> :** ban the user.\n\n**{prefix}changeprefix <newPrefix> :** Change the bot's prefix for the guild.", inline=False)
            embed.add_field(name=f"__COMMANDS :__", value=f"**{prefix}userinfos <@user/ID> :** Get user infomations.", inline=False)
            embed.set_footer(text="Bot Created by Darkempire#8245")
            await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))