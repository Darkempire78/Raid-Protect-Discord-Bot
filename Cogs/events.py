from discord.ext import commands
from discord.ext.commands import MissingPermissions, CommandNotFound, BotMissingPermissions, MissingRequiredArgument

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
                await ctx.send('This command has a cooldown, be sure to wait for '+str(day)+ "day(s)")
            elif hour > 0:
                await ctx.send('This command has a cooldown, be sure to wait for '+str(hour)+ " hour(s)")
            elif minute > 0:
                await ctx.send('This command has a cooldown, be sure to wait for '+ str(minute)+" minute(s)")
            else:
                await ctx.send(f'This command has a cooldown, be sure to wait for {error.retry_after:.2f} second(s)')
        elif isinstance(error, BotMissingPermissions):
            missing = ", ".join(error.missing_perms)
            return await ctx.send(f"{ctx.author.mention} I need the `{missing}` permission(s) to run this command.")
        elif isinstance(error, MissingPermissions):
            missing = ", ".join(error.missing_perms)
            return await ctx.send(f"{ctx.author.mention} You need the `{missing}` permission(s) to run this command.")
        elif isinstance(error, MissingRequiredArgument):
            return await ctx.send(f"{ctx.author.mention} Required argument is missed!\nUse this model : `{self.bot.command_prefix}{ctx.command.name} {ctx.command.usage}`")
        else:
            await ctx.send(error)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(EventsCog(bot))