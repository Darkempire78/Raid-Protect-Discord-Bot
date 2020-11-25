import discord
import json

from discord.ext import commands
from discord.utils import get

async def sendLogMessage(self, event, channel, embed, messageFile=None):
    """Send the message in the log channel"""
    if channel == False:
        # Logs are disbaled
        return 
    else:
        if isinstance(channel, int):
            # It is a channel id
            channel = self.bot.get_channel(channel)

        if channel == None:
            # Channel is deleted
            try:
                channel = await event.guild.create_text_channel(f"{self.bot.user.name}-logs")
                await channel.set_permissions(event.guild.default_role, read_messages=False)
            except Exception as error:
                if error.code == 50013:
                    return await event.channel.send(f"**Log error :** I can not create a log channel ({error.text}).")
                else:
                    return await event.channel.send(error.text)

            # Get configuration.json data 
            with open("configuration.json", "r") as config:
                data = json.load(config)
                data["logChannel"] = channel.id

            # Edit configuration.json
            newdata = json.dumps(data, indent=4, ensure_ascii=False)
            with open("configuration.json", "w") as config:
                config.write(newdata)

        # Send the message
        await channel.send(embed=embed, file=messageFile)