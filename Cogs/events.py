from discord.ext import commands
from discord.ext.commands import MissingPermissions, CommandNotFound, BotMissingPermissions, MissingRequiredArgument
from Tools.utils import getGuildPrefix

# ------------------------ COGS ------------------------ #  

class EventsCog(commands.Cog, name="EventsCog"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------- #

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            day = round(error.retry_after/86400)
            hour = round(error.retry_after/3600)
            minute = round(error.retry_after/60)
            if day > 0:
                await ctx.send(self.bot.translate.msg(ctx.guild.id, "events", "COMMAND_IN_COOLDOWN_DAY").format(day))
            elif hour > 0:
                await ctx.send(self.bot.translate.msg(ctx.guild.id, "events", "COMMAND_IN_COOLDOWN_HOUR").format(hour))
            elif minute > 0:
                await ctx.send(self.bot.translate.msg(ctx.guild.id, "events", "COMMAND_IN_COOLDOWN_MINUTE").format(minute))
            else:
                await ctx.send(self.bot.translate.msg(ctx.guild.id, "events", "COMMAND_IN_COOLDOWN_SECOND").format(round(error.retry_after)))
        elif isinstance(error, BotMissingPermissions):
            missing = ", ".join(error.missing_perms)
            return await ctx.send(self.bot.translate.msg(ctx.guild.id, "events", "BOT_MISSING_PERMISSIONS").format(ctx.author.mention, missing))
        elif isinstance(error, MissingPermissions):
            missing = ", ".join(error.missing_perms)
            return await ctx.send(self.bot.translate.msg(ctx.guild.id, "events", "MISSING_PERMISSIONS").format(ctx.author.mention, missing))
        elif isinstance(error, MissingRequiredArgument):
            prefix = getGuildPrefix()
            return await ctx.send(self.bot.translate.msg(ctx.guild.id, "events", "MISSING_REQUIRED_ARGUMENT").format(ctx.author.mention, prefix, ctx.command.name, ctx.command.usage))
        else:
            await ctx.send(error)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(EventsCog(bot))