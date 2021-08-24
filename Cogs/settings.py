import discord
import json
from Tools.utils import getConfig
from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class SettingsCog(commands.Cog, name="settings command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'settings',
                        description="Display the settings.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def settings (self, ctx):

        data = getConfig()
        captcha = data["captcha"] 
        captchaChannel = data["captchaChannel"]  
        logChannel = data["logChannel"]
        temporaryRole = data["temporaryRole"]
        roleGivenAfterCaptcha = data["roleGivenAfterCaptcha"]
        minAccountAge = data["minAccountDate"]
        antispam = data["antiSpam"]
        allowSpam = data["allowSpam"]
        antiNudity = data["antiNudity"]
        antiProfanity =  data["antiProfanity"]
            
        minAccountAge = int(minAccountAge/3600)

        allowSpam2= ""
        if len(allowSpam) == 0:
            allowSpam2 = "None"
        else:
            for x in allowSpam:
                allowSpam2 = f"{allowSpam2}<#{x}>, "

        if roleGivenAfterCaptcha is not False:
            roleGivenAfterCaptcha = f"<@&{roleGivenAfterCaptcha}>"
        if captchaChannel is not False:
            captchaChannel = f"<#{captchaChannel}>"
        if logChannel is not False:
            logChannel = f"<#{logChannel}>"
            
        embed = discord.Embed(title=f"**SERVER SETTINGS**", description=f"[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)", color=0xdeaa0c)
        embed.add_field(name= f"**CAPTCHA PROTECTION** - ``({self.bot.command_prefix}setup <on/off>)``", value= f"Captcha enabled : **{captcha}**\nCaptcha channel : {captchaChannel}\nBot logs : {logChannel}\nTemporary role : <@&{temporaryRole}>", inline=False)
        embed.add_field(name= f"**ROLE GIVEN AFTER CAPTCHA** - ``({self.bot.command_prefix}giveroleaftercaptcha <role ID/off>)``", value= f"Role given after captcha : **{roleGivenAfterCaptcha}**", inline=False)
        embed.add_field(name= f"**MINIMUM ACCOUNT AGE** - ``({self.bot.command_prefix}minaccountage <number (hours)>)``", value= f"Minimum account age : **{minAccountAge} hours**", inline=False)
        embed.add_field(name= f"**ANTI SPAM** - ``({self.bot.command_prefix}antispam <true/false>)``", value= f"Anti spam enabled : **{antispam}**", inline=False)
        embed.add_field(name= f"**ALLOW SPAM** - ``({self.bot.command_prefix}allowspam <#channel> (remove))``", value= f"Channel where spam is allowed : **{allowSpam2[:-2]}**", inline=False)
        embed.add_field(name= f"**ANTI NUDITY** - ``({self.bot.command_prefix}antinudity <true/false>)``", value= f"Anti nudity image enabled : **{antiNudity}**", inline=False)
        embed.add_field(name= f"**ANTI PROFANITY** - ``({self.bot.command_prefix}antiprofanity <true/false>)``", value= f"Anti profanity enabled : **{antiProfanity}**", inline=False)
        embed.set_footer(text="Bot Created by Darkempire#8245")
        return await ctx.channel.send(embed=embed)


# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(SettingsCog(bot))