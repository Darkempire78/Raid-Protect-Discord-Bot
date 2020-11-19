import discord
import json
import requests

from discord.ext import commands
from discord.utils import get

from datetime import datetime, timedelta

import nude
from nude import Nude
from PIL import Image
from io import BytesIO, IOBase


class Nude2(Nude):
    """Repare the module error"""
    def __init__(self, path_or_io):
        self.image = Image.open(path_or_io)
        bands = self.image.getbands()
        # convert greyscale to rgb
        if len(bands) == 1:
            new_img = Image.new("RGB", self.image.size)
            new_img.paste(self.image)
            f = self.image.filename
            self.image = new_img
            self.image.filename = f
        self.skin_map = []
        self.skin_regions = []
        self.detected_regions = []
        self.merge_regions = []
        self.last_from, self.last_to = -1, -1
        self.result = None
        self.message = None
        self.width, self.height = self.image.size
        self.total_pixels = self.width * self.height

# ------------------------ COGS ------------------------ #  
class OnMessageCog(commands.Cog, name="on message"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.Cog.listener()
    async def on_message(self, message):

        # Anti spam
        if message.author.bot:
            return

        if message.content == "" and len(message.attachments) == 0:
            return

        # Nudity check     
        if (message.channel.nsfw != True) and (len(message.attachments) > 0):
            # Use : https://github.com/hhatto/nude.py
            # Other option : https://github.com/notAI-tech/NudeNet (untested)
            for i in message.attachments:
                # Check if the attachment is an image
                if i.filename.endswith((".png", ".jpg", ".jpeg")):
                    
                    # Data
                    with open("configuration.json", "r") as config:
                        data = json.load(config) 
                        antiNudity = data["antiNudity"]

                    if antiNudity == True:  
                        try:
                            logChannel = self.bot.get_channel(data["logChannel"])

                            # Convert the image to io
                            response = requests.get(i.url)
                            image_bytes = BytesIO(response.content)
                            # Check the image
                            n = Nude2(image_bytes)
                            n.parse()
                            
                            if n.result == True:
                                # Logs
                                i.filename = f"SPOILER_{i.filename}"
                                spoiler = await i.to_file()
                                embed = discord.Embed(title = f"**{message.author} has sent a nudity image.**", description = f"In {message.channel.mention}.\n\n**__User informations :__**\n\n**Name :** {message.author}\n**Id :** {message.author.id}\n\n**The image :**", color = 0xff0000)
                                await logChannel.send(file=spoiler, embed=embed)

                                # embed = discord.Embed(title = f"**{message.author} has sent a nudity image.**", description = f"In {message.channel.mention}.\n\n**__User informations :__**\n\n**Name :** {message.author}\n**Id :** {message.author.id}\n\n**The image :**", color = 0xff0000)
                                # embed.set_image(url=i.url)
                                # await logChannel.send(embed = embed)
                                
                                # Delete
                                await message.delete()
                                await message.channel.send(f"{message.author.mention} do not send nudity image !")
                        except:
                            print("Nudity check : error")
        # Data
        with open("configuration.json", "r") as config:
            data = json.load(config) 
            antiSpam = data["antiSpam"] 
            allowSpam = data["allowSpam"]
            logChannel = self.bot.get_channel(data["logChannel"])

        # Anti profanity
        # from profanity_check import predict, predict_prob
        # test = predict_prob(message.content)
        # print(test)

        # Anti spam
        if antiSpam == True:
            def check (message):
                return (message.author == message.author and (datetime.utcnow() - message.created_at).seconds < 15)

            if message.author.guild_permissions.administrator:
                return 

            if message.channel.id in allowSpam:
                return
                
            if len(list(filter(lambda m: check(m), self.bot.cached_messages))) >= 8 and len(list(filter(lambda m: check(m), self.bot.cached_messages))) < 12:
                await message.channel.send(f"{message.author.mention} Stop spam please!")
            elif len(list(filter(lambda m: check(m), self.bot.cached_messages))) >= 12:
                embed = discord.Embed(title = f"**YOU HAVE BEEN KICKED FROM {message.author.guild.name}**", description = f"Reason : You spammed.", color = 0xff0000)
                await message.author.send(embed = embed)
                await message.author.kick() # Kick the user
                await message.channel.send(f"{message.author.mention} was kicked for spamming !")
                
                # Logs
                # Create a hastbin file
                messageNumber = 0
                logTime = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
                logs = f"[LOGS] {self.bot.user.name.upper()} - ANTI-SPAM \n\n{message.author} ({message.author.id}) spammed in #{message.channel} the {logTime}\n\n"
                
                for i in  self.bot.cached_messages:
                    if i.author.id == message.author.id and i.content != "":
                        messageNumber += 1
                        logs = f"{logs}\n[{messageNumber}] {i.content}"

                url = 'https://hastebin.com'
                hastbin = requests.post(f'{url}/documents', data=logs).json()
                hastbinUrl = url + "/" + hastbin['key']
                try:
                    embed = discord.Embed(title = f"**{message.author} has been kicked.**", description = f"**Reason :** He spammed in {message.channel.mention}.\n\n**__User informations :__**\n\n**Name :** {message.author}\n**Id :** {message.author.id}\n\n**Logs :** {hastbinUrl}", color = 0xff0000)
                    await logChannel.send(embed = embed)
                except:
                    pass

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(OnMessageCog(bot))