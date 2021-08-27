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

                perms = channel.overwrites_for(temporaryRole)
                perms.read_messages=False
                await channel.set_permissions(temporaryRole, overwrite=perms)

            elif isinstance(channel, discord.VoiceChannel):

                perms = channel.overwrites_for(temporaryRole)
                perms.read_messages=False
                perms.connect=False
                await channel.set_permissions(temporaryRole, overwrite=perms)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(OnChannelCreate(bot))