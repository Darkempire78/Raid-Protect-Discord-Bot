#!/usr/bin/env python3

import discord
import random 
import asyncio
import time
import os
import sys
import json

from datetime import datetime
from discord.ext import commands
from discord.ext import tasks

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot("?", intents = intents)
# bot = commands.when_mentioned_or("?")

# HELP
bot.remove_command("help") # To create a personal help command 

# Load cogs
path = os.path.realpath(__file__)
path = path.replace('\\', '/')
path = path.replace('main.py', 'Cogs')
initial_extensions = os.listdir(path)
try:
    initial_extensions.remove("__pycache__")
except:
    pass
print(initial_extensions)
initial_extensions3 = []
for initial_extensions2 in initial_extensions:
    initial_extensions2 = "Cogs." + initial_extensions2
    initial_extensions2 = initial_extensions2.replace(".py", "")
    initial_extensions3.append(initial_extensions2)

if __name__ == '__main__':
    for extension in initial_extensions3:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))
    print(discord.__version__)


# ------------------------ RUN ------------------------ # 
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
bot.run(token)