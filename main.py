#!/usr/bin/env python3

import discord
import os
import json
import datetime

from discord.ext import commands


def utc2jst(t):
    return t + datetime.timedelta(hours=9)


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot("?", intents=intents)

# bind utility function
bot.utc2jst = utc2jst

# bot = commands.when_mentioned_or("?")
# HELP
bot.remove_command("help")  # To create a personal help command

# Load cogs
if __name__ == '__main__':
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"))
    print(discord.__version__)


# ------------------------ RUN ------------------------ #
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
bot.run(token)
