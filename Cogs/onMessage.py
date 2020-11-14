import discord
import json

from discord.ext import commands
from discord.utils import get

from datetime import datetime, timedelta


# ------------------------ COGS ------------------------ #  

class OnMessageCog(commands.Cog, name="on message"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.Cog.listener()
    async def on_message(self, message):

        # Anti spam
        if message.author.bot or message.content == "":
            return
            
        # 
        with open("configuration.json", "r") as config:
            data = json.load(config) 
            antiSpam = data["antiSpam"] 
            allowSpam = data["allowSpam"]
            logChannel = self.bot.get_channel(data["logChannel"])

        if antiSpam == True:
            def check (message):
                return (message.author == message.author and (datetime.utcnow() - message.created_at).seconds < 15)

            if message.author.guild_permissions.administrator:
                return 

            if message.channel.id in allowSpam:
                return
            print("message nb", len(list(filter(lambda m: check(m), self.bot.cached_messages))))
            if len(list(filter(lambda m: check(m), self.bot.cached_messages))) >= 8 and len(list(filter(lambda m: check(m), self.bot.cached_messages))) < 12:
                await message.channel.send(f"{message.author.mention} Stop spam please!")
            elif len(list(filter(lambda m: check(m), self.bot.cached_messages))) >= 12:
                embed = discord.Embed(title = f"**YOU HAVE BEEN KICKED FROM {message.author.guild.name}**", description = f"Reason : You spammed.", color = 0xff0000)
                await message.author.send(embed = embed)
                await message.author.kick() # Kick the user
                await message.channel.send(f"{message.author.mention} was kicked for spamming !")
                # Logs
                try:
                    embed = discord.Embed(title = f"**{message.author} has been kicked.**", description = f"**Reason :** He spammed in {message.channel}.\n\n**__User informations :__**\n\n**Name :** {message.author}\n**Id :** {message.author.id}", color = 0xff0000)
                    await logChannel.send(embed = embed)
                except:
                    pass

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(OnMessageCog(bot))

