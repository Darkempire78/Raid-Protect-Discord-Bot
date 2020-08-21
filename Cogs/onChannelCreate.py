import discord
import os
import shutil
import json

from discord.ext import commands
from discord.utils import get


# ------------------------ COGS ------------------------ #  

class OnChannelCreate(commands.Cog, name="on channel create"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        with open("configuration.json", "r") as config:
            data = json.load(config)
            temporaryRole = get(channel.guild.roles, id= data["temporaryRole"])

        if temporaryRole == None:
            pass

        else:
            for channel in channel.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    await channel.set_permissions(temporaryRole, read_messages=False)
                elif isinstance(channel, discord.VoiceChannel):
                    await channel.set_permissions(temporaryRole, read_messages=False, connect=False)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(OnChannelCreate(bot))

