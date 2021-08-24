import discord
import json
from Tools.utils import getConfig
from discord.ext import commands
from discord.utils import get


# ------------------------ COGS ------------------------ #  

class OnChannelCreate(commands.Cog, name="on channel create"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        data = getConfig(channel.guild.id)
        temporaryRole = get(channel.guild.roles, id= data["temporaryRole"])

        if temporaryRole is not None:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(temporaryRole, read_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(temporaryRole, read_messages=False, connect=False)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(OnChannelCreate(bot))