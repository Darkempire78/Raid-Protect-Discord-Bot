#!/usr/bin/env python3

import discord
import os
import json
from discord.ext.commands import AutoShardedBot as asb
from discord.ext import commands

loaded = False

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

class RaidProtect(asb):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("?"),
            case_insensitive=True, # makes it so it doesnt matter if a command is capitalised or not
            intents=discord.Intents.all(), # remove this if you dont want to enable all intents
            help_command=None # dont remove this lol
        )
        
        self.remove_command("help")
        self.cog_blacklist = [ # add more if you dont want to load them
            "__init__.py",
            "functions.py"
        ]
        
        if not loaded:
            for file in os.listdir("./Cogs"):
                if file.endswith(".py") and file not in self.cog_blacklist:
                    try:
                        self.load_extension(f"Cogs.{file[:-3]}")
                    except Exception as e:
                        print(str(e))
            loaded = True # using this so it doesnt reload cogs when getting variables


    async def on_connect(self):
        print("Connected")
    async def on_ready(self):
        print("Ready")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{self.get_prefix}help"))

    # no need to add unimportant stuff


if __name__ == "__main__":
    with open("configuration.json", "r") as f:
        config = json.load(f)
    bot = RaidProtect()
    bot.run(config["token"])
