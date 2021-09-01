import discord
import json
from discord.ext import commands
from Tools.utils import getConfig, updateConfig

# ------------------------ COGS ------------------------ #  

class ChangePrefixCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'changelanguage', 
                        aliases= ["language"],
                        usage="<language>",
                        description="Change the bot's language.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def changelanguage(self, ctx, language):

        availableLanguage = [
            "en-US",
            "fr-FR"
        ]

        if language not in availableLanguage:
            return ctx.send(self.bot.translate.msg(ctx.guild.id, "changelanguage", "INVALID_LANGUAGE_SELECTED").format(str(availableLanguage)))
            
        data = getConfig(ctx.guild.id)
        data["language"] = language

        await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "changelanguage", "NEW_LANGUAGE").format(language))
        
        updateConfig(ctx.guild.id, data)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(ChangePrefixCog(bot))