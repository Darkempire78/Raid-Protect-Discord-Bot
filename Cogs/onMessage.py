import discord
import json
import aiohttp
from discord.ext import commands
from datetime import datetime
from nude import Nude
from io import BytesIO
from profanity_check import predict
from Tools.utils import getConfig
from Tools.logMessage import sendLogMessage

# ------------------------ COGS ------------------------ #  
class OnMessageCog(commands.Cog, name="on message"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.Cog.listener()
    async def on_message(self, message):

        # If bot or Administrator
        if message.author.bot or message.author.guild_permissions.administrator is True:
            return

        if message.content == "" and len(message.attachments) == 0:
            return

        # Nudity check     
        if (message.channel.nsfw is not True) and (len(message.attachments) > 0):
            # Used : https://github.com/hhatto/nude.py
            # Other option : https://github.com/notAI-tech/NudeNet (untested)
            for i in message.attachments:
                # Check if the attachment is an image
                if i.filename.endswith((".png", ".jpg", ".jpeg")):
                    
                    # Data
                    data = getConfig(message.guild.id)
                    antiNudity = data["antiNudity"]

                    if antiNudity is True:  
                        logChannel = data["logChannel"]

                        # Get the image
                        async with aiohttp.ClientSession() as session:
                            async with session.get(i.url) as response:
                                image_bytes = await response.read()
                        
                        # Convert the image to io
                        image_bytes = BytesIO(image_bytes)
                        
                        # Check the image
                        n = Nude(image_bytes)
                        n.parse()
                        
                        if n.result is True:
                            # Logs
                            i.filename = f"SPOILER_{i.filename}"
                            spoiler = await i.to_file()
                            embed = discord.Embed(title = self.bot.translate.msg(message.guild.id, "onMessage", "USER_HAS_SENT_NUDITY").format(message.author), description = self.bot.translate.msg(message.guild.id, "onMessage", "USER_HAS_SENT_NUDITY_DESCRIPTION").format(message.channel.mention, message.author, message.author.id), color = 0xff0000)
                            await sendLogMessage(self, event=message, channel=logChannel, embed=embed, messageFile=spoiler)
                            
                            # Delete
                            await message.delete()
                            await message.channel.send(self.bot.translate.msg(message.guild.id, "onMessage", "DO_NOT_SEND_NUDITY").format(message.author.mention))
        
        # Data
        data = getConfig(message.guild.id)
        antiProfanity =  data["antiProfanity"]
        antiSpam = data["antiSpam"] 
        allowSpam = data["allowSpam"]
        logChannel = data["logChannel"]

        # Anti profanity
        if antiProfanity is True:
            words = []
            words.append(message.content)
            profanity = predict(words) # profanity2 = predict_prob(words)
            if profanity[0] == 1:
                await message.delete()
                await message.channel.send(self.bot.translate.msg(message.guild.id, "onMessage", "DO_NOT_INSULT").format(message.author.mention))
                # Logs
                if len(message.content) > 1600:
                    message.content = message.content + "..."
                embed = discord.Embed(title = self.bot.translate.msg(message.guild.id, "onMessage", "USER_HAS_SENT_PROFANITY").format(message.author), description = self.bot.translate.msg(message.guild.id, "onMessage", "USER_HAS_SENT_PROFANITY_DESCRIPTION").format(message.channel.mention, message.author, message.author.id, message.content), color = 0xff0000)
                await sendLogMessage(self, event=message, channel=logChannel, embed=embed)

        # Anti spam
        if antiSpam is True:
            def check (message):
                return (message.author == message.author and (datetime.utcnow() - message.created_at).seconds < 15)

            if message.author.guild_permissions.administrator:
                return 

            if message.channel.id in allowSpam:
                return
                
            if len(list(filter(lambda m: check(m), self.bot.cached_messages))) >= 8 and len(list(filter(lambda m: check(m), self.bot.cached_messages))) < 12:
                await message.channel.send(self.bot.translate.msg(message.guild.id, "onMessage", "STOP_SPAM").format(message.author.mention))
            elif len(list(filter(lambda m: check(m), self.bot.cached_messages))) >= 12:
                embed = discord.Embed(title = self.bot.translate.msg(message.guild.id, "onMessage", "YOU_HAVE_BEEN_KICKED").format(message.author.guild.name), description =self.bot.translate.msg(message.guild.id, "onMessage", "YOU_HAVE_BEEN_KICKED_SPAM_REASON"), color = 0xff0000)
                await message.author.send(embed = embed)
                await message.author.kick() # Kick the user
                await message.channel.send(self.bot.translate.msg(message.guild.id, "onMessage", "USER_HAS_BEEN_KICKED_FOR_SPAMMING").format(message.author.mention))
                
                # Logs -> Create a hastbin file
                logTime = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
                logs = f"[LOGS] {self.bot.user.name.upper()} - ANTI-SPAM \n\n{message.author} ({message.author.id}) spammed in \"{message.channel}\" the {logTime}\n\n"
                messageNumber = 0

                # Get user messages
                user_cache_messages = [i for i in self.bot.cached_messages if i.author.id == message.author.id]
                
                for i in user_cache_messages[-10:]:
                    messageNumber += 1
                    logs = f"{logs}\n[{messageNumber}] {i.content}"

                url = 'https://hastebin.com'
                async with aiohttp.ClientSession() as session:
                    async with session.post(f'{url}/documents', data=logs) as hastbin:
                        hastbin = await hastbin.json()
                        hastbinUrl = url + "/" + hastbin['key']
                
                embed = discord.Embed(title = self.bot.translate.msg(message.guild.id, "onMessage", "MEMBER_HAS_BEEN_KICKED").format(message.author), description = self.bot.translate.msg(message.guild.id, "onMessage", "USER_HAS_BEEN_KICKED_FOR_SPAMMING_LOG").format(message.channel.mention, message.author, message.author.id, hastbinUrl), color = 0xff0000)
                await sendLogMessage(self, event=message, channel=logChannel, embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(OnMessageCog(bot))