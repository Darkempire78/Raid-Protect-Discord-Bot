import discord
import random 
import asyncio
import time
import os
import datetime

from datetime import datetime
from discord.ext import commands
from discord.ext.commands import MissingPermissions, CheckFailure, CommandNotFound

# ------------------------ COGS ------------------------ #  

class EventsCog(commands.Cog, name="EventsCog"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------- #

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
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
        elif isinstance(error, CommandNotFound):
            return
        elif isinstance(error, MissingPermissions):
            await ctx.send(error.text)
        elif isinstance(error, CheckFailure):
            await ctx.send(error.original.text)
        else:
            await ctx.send(error)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(EventsCog(bot))