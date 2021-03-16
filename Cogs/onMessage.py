import json
from datetime import datetime
from io import BytesIO

import aiohttp
import discord
from discord.ext import commands
from nude import Nude
from profanity_check import predict

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
                    with open("configuration.json", "r") as config:
                        data = json.load(config)
                        anti_nudity = data["antiNudity"]

                    if anti_nudity is True:
                        log_channel = data["logChannel"]

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
                            embed = discord.Embed(title=f"**{message.author}がわいせつな画像を送信しました。**",
                                                  description=f"チャンネル：{message.channel.mention}\n\n"
                                                              f"**ユーザー情報 :__**\n\n"
                                                              f"**名前 :** {message.author}\n"
                                                              f"**Id :** {message.author.id}\n\n"
                                                              f"**該当の画像 :**",
                                                  color=0xff0000)
                            await sendLogMessage(self, event=message, channel=log_channel, embed=embed,
                                                 messageFile=spoiler)

                            # embed = discord.Embed(title = f"**{message.author} has sent a nudity image.**",
                            # description = f"In {message.channel.mention}.\n\n**__User informations :__**\n\n**Name
                            # :** {message.author}\n**Id :** {message.author.id}\n\n**The image :**",
                            # color = 0xff0000) embed.set_image(url=i.url) await logChannel.send(embed = embed)

                            # Delete
                            await message.delete()
                            await message.channel.send(f"{message.author.mention} わいせつな画像をそうしんしないで下さい！")

        # Data
        with open("configuration.json", "r") as config:
            data = json.load(config)
            anti_profanity = data["antiProfanity"]
            anti_spam = data["antiSpam"]
            allow_spam = data["allowSpam"]
            log_channel = data["logChannel"]

        # Anti profanity
        if anti_profanity is True:
            words = [message.content]
            profanity = predict(words)  # profanity2 = predict_prob(words)
            if profanity[0] == 1:
                await message.delete()  # Delete
                await message.channel.send(f"{message.author.mention} Do not insult!")
                # Logs
                if len(message.content) > 1600:
                    message.content = message.content + "..."
                embed = discord.Embed(title=f"**{message.author}が侮辱を含んだメッセージを送信しました。**",
                                      description=f"チャンネル：{message.channel.mention}.\n\n"
                                                  f"**__ユーザー情報 :__**\n\n"
                                                  f"**名前 :** {message.author}\n"
                                                  f"**Id :** {message.author.id}\n\n"
                                                  f"**該当のメッセージ :**\n\n{message.content}",
                                      color=0xff0000)
                await sendLogMessage(self, event=message, channel=log_channel, embed=embed)

        # Anti spam
        if anti_spam is True:
            def check(passed_message):
                return passed_message.author == passed_message.author and \
                       (datetime.utcnow() - passed_message.created_at).seconds < 15

            if message.author.guild_permissions.administrator:
                return

            if message.channel.id in allow_spam:
                return

            if len(list(filter(lambda m: check(m), self.bot.cached_messages))) >= 8 and len(
                    list(filter(lambda m: check(m), self.bot.cached_messages))) < 12:
                await message.channel.send(f"{message.author.mention} Stop spam please!")
            elif len(list(filter(lambda m: check(m), self.bot.cached_messages))) >= 12:
                embed = discord.Embed(title=f"**YOU HAVE BEEN KICKED FROM {message.author.guild.name}**",
                                      description=f"Reason : You spammed.", color=0xff0000)
                await message.author.send(embed=embed)
                await message.author.kick()  # Kick the user
                await message.channel.send(f"{message.author.mention} was kicked for spamming !")

                # Logs -> Create a hastbin file
                log_time = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
                logs = f"[LOGS] {self.bot.user.name.upper()} - ANTI-SPAM \n\n" \
                       f"{message.author} ({message.author.id}) spammed in \"{message.channel}\" the {log_time}\n\n"
                message_number = 0

                # Get user messages
                user_cache_messages = [i for i in self.bot.cached_messages if i.author.id == message.author.id]

                for i in user_cache_messages[-10:]:
                    message_number += 1
                    logs = f"{logs}\n[{message_number}] {i.content}"

                url = 'https://hastebin.com'
                async with aiohttp.ClientSession() as session:
                    async with session.post(f'{url}/documents', data=logs) as hastbin:
                        hastbin = await hastbin.json()
                        hastbin_url = url + "/" + hastbin['key']

                embed = discord.Embed(title=f"**{message.author}がキックされました。**",
                                      description=f"**理由 :**{message.channel.mention}でスパムを行いました。\n\n"
                                                  f"**__ユーザー情報 :__**\n\n"
                                                  f"**名前 :** {message.author}\n"
                                                  f"**Id :** {message.author.id}\n\n"
                                                  f"**ログ :** {hastbin_url}",
                                      color=0xff0000)
                await sendLogMessage(self, event=message, channel=log_channel, embed=embed)


# ------------------------ BOT ------------------------ #

def setup(bot):
    bot.add_cog(OnMessageCog(bot))
