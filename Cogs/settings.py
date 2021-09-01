import discord
from Tools.utils import getConfig, getGuildPrefix
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

        data = getConfig(ctx.guild.id)
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
        language =  data["language"]
            
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

        prefix = await getGuildPrefix(self.bot, ctx)

        embed = discord.Embed(title=self.bot.translate.msg(ctx.guild.id, "settings", "SERVER_SETTINGS"), description=f"[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)", color=0xdeaa0c)
        embed.add_field(name= self.bot.translate.msg(ctx.guild.id, "settings", "CAPTCHA_PROTECTION").format(prefix), value= self.bot.translate.msg(ctx.guild.id, "settings", "CAPTCHA_PROTECTION_DESCRIPTION").format(captcha, captchaChannel, logChannel, temporaryRole), inline=False)
        embed.add_field(name= self.bot.translate.msg(ctx.guild.id, "settings", "ROLE_GIVEN_AFTER_CAPTCHA").format(prefix), value= self.bot.translate.msg(ctx.guild.id, "settings", "ROLE_GIVEN_AFTER_CAPTCHA_DESCRIPTION").format(roleGivenAfterCaptcha), inline=False)
        embed.add_field(name= self.bot.translate.msg(ctx.guild.id, "settings", "MINIMUM_ACCOUNT_AGE").format(prefix), value= self.bot.translate.msg(ctx.guild.id, "settings", "MINIMUM_ACCOUNT_AGE_DESCRIPTION").format(minAccountAge), inline=False)
        embed.add_field(name= self.bot.translate.msg(ctx.guild.id, "settings", "ANTI_SPAM").format(prefix), value= self.bot.translate.msg(ctx.guild.id, "settings", "ANTI_SPAM_DESCRIPTION").format(antispam), inline=False)
        embed.add_field(name= self.bot.translate.msg(ctx.guild.id, "settings", "ALLOW_SPAM").format(prefix), value= self.bot.translate.msg(ctx.guild.id, "settings", "ALLOW_SPAM_DESCRIPTION").format(allowSpam2[:-2]), inline=False)
        embed.add_field(name= self.bot.translate.msg(ctx.guild.id, "settings", "ANTI_NUDITY").format(prefix), value= self.bot.translate.msg(ctx.guild.id, "settings", "ANTI_NUDITY_DESCRIPTION").format(antiNudity), inline=False)
        embed.add_field(name= self.bot.translate.msg(ctx.guild.id, "settings", "ANTI_PROFANITY").format(prefix), value= self.bot.translate.msg(ctx.guild.id, "settings", "ANTI_PROFANITY_DESCRIPTION").format(antiProfanity), inline=False)
        embed.set_footer(text=self.bot.translate.msg(ctx.guild.id, "global", "BOT_CREATOR"))
        return await ctx.channel.send(embed=embed)


# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(SettingsCog(bot))