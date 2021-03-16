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
            jour = round(error.retry_after/86400)
            heure = round(error.retry_after/3600)
            minute = round(error.retry_after/60)
            if jour > 0:
                await ctx.send(f'このコマンドはクールダウン中です。 あと{jour}日待ってから実行してください')
            elif heure > 0:
                await ctx.send(f'このコマンドはクールダウン中です。 あと{heure}時間待ってから実行してください')
            elif minute > 0:
                await ctx.send(f'このコマンドはクールダウン中です。 あと{minute}分待ってから実行してください')
            else:
                await ctx.send(f'このコマンドはクールダウン中です。 あと{error.retry_after:.2f}秒待ってから実行してください')
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
