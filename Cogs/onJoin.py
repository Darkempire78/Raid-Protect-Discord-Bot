import discord
import json
import numpy as np
import random
import string
import Augmentor
import os
import shutil
import asyncio
import time

from discord.ext import commands
from discord.utils import get

from datetime import datetime
from random import choice
from PIL import ImageFont, ImageDraw, Image

from Tools.logMessage import sendLogMessage

# ------------------------ COGS ------------------------ #


class OnJoinCog(commands.Cog, name="on join"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if (member.bot):
            return

        # Read configuration.json
        with open("configuration.json", "r") as config:
            data = json.load(config)
            logChannel = data["logChannel"]
            captchaChannel = self.bot.get_channel(data["captchaChannel"])

        mja_at = self.bot.utc2jst(member.joined_at)
        memberTime = f"{mja_at.year}-{mja_at.month}-{mja_at.day} {mja_at.hour}:{mja_at.minute}:{mja_at.second}"

        # Check the user account creation date (1 day by default)
        if data["minAccountDate"] is False:
            userAccountDate = member.created_at.timestamp()
            if userAccountDate < data["minAccountDate"]:
                minAccountDate = data["minAccountDate"] / 3600
                embed = discord.Embed(title=f"**あなたは {member.guild.name} からキックされました**",
                                      description=f"**理由**: **あなたのアカウントは作成後{minAccountDate}時間しか経っていないため。**", color=0xff0000)
                await member.send(embed=embed)
                await member.kick()  # Kick the user
                # Logs
                embed = discord.Embed(
                    title=f"**{member} がキックされました**", description=f"**理由**: **当アカウントは作成後{minAccountDate}時間しか経過していないため**\nアカウント作成日時 : {self.bot.utc2jst(member.created_at)}\n\n**__ユーザー情報 :__**\n\n**名前 :** {member}\n**ID :** {member.id}", color=0xff0000)
                embed.set_footer(
                    text=f"at {self.bot.utc2jst(member.joined_at)}")
                await sendLogMessage(self, event=member, channel=logChannel, embed=embed)

        if data["captcha"] is True:

            # Give temporary role
            getrole = get(member.guild.roles, id=data["temporaryRole"])
            await member.add_roles(getrole)

            # Create captcha
            image = np.zeros(shape=(100, 350, 3), dtype=np.uint8)

            # Create image
            image = Image.fromarray(image+255)  # +255 : black to white

            # Add text
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(font="Tools/arial.ttf", size=60)

            # + string.ascii_lowercase + string.digits
            text = ' '.join(random.choice(string.ascii_uppercase)
                            for _ in range(6))

            # Center the text
            W, H = (350, 100)
            w, h = draw.textsize(text, font=font)
            draw.text(((W-w)/2, (H-h)/2), text, font=font, fill=(90, 90, 90))

            # Save
            ID = member.id
            folderPath = f"captchaFolder/captcha_{ID}"
            try:
                os.mkdir(folderPath)
            except:
                if os.path.isdir('captchaFolder') is False:
                    os.mkdir("captchaFolder")
                if os.path.isdir(folderPath) is True:
                    shutil.rmtree(folderPath)
                os.mkdir(folderPath)
            image.save(f"{folderPath}/captcha{ID}.png")

            # Deform
            p = Augmentor.Pipeline(folderPath)
            p.random_distortion(probability=1, grid_width=4,
                                grid_height=4, magnitude=14)
            p.process()

            # Search file in folder
            path = f"{folderPath}/output"
            files = os.listdir(path)
            captchaName = [i for i in files if i.endswith('.png')]
            captchaName = captchaName[0]

            image = Image.open(f"{folderPath}/output/{captchaName}")

            # Add line
            width = random.randrange(6, 8)
            co1 = random.randrange(0, 75)
            co3 = random.randrange(275, 350)
            co2 = random.randrange(40, 65)
            co4 = random.randrange(40, 65)
            draw = ImageDraw.Draw(image)
            draw.line([(co1, co2), (co3, co4)], width=width, fill=(90, 90, 90))

            # Add noise
            noisePercentage = 0.25  # 25%

            pixels = image.load()  # create the pixel map
            for i in range(image.size[0]):  # for every pixel:
                for j in range(image.size[1]):
                    rdn = random.random()  # Give a random %
                    if rdn < noisePercentage:
                        pixels[i, j] = (90, 90, 90)

            # Save
            image.save(f"{folderPath}/output/{captchaName}_2.png")

            # Send captcha
            captchaFile = discord.File(
                f"{folderPath}/output/{captchaName}_2.png")
            captchaEmbed = await captchaChannel.send(f"**サーバーに参加するためには認証してください :**\n{member.mention}, 認証コードを入力することでサーバーにアクセスできます。", file=captchaFile)
            # Remove captcha folder
            try:
                shutil.rmtree(folderPath)
            except Exception as error:
                print(f"Delete captcha file failed {error}")

            # Check if it is the right user
            def check(message):
                if message.author == member and message.content != "":
                    return message.content

            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check)
                # Check the captcha
                password = text.split(" ")
                password = "".join(password)
                if msg.content == password:

                    embed = discord.Embed(
                        description=f"{member.mention} 認証に成功しました", color=0x2fa737)  # Green
                    await captchaChannel.send(embed=embed, delete_after=5)
                    # Give and remove roles
                    try:
                        getrole = get(member.guild.roles,
                                      id=data["roleGivenAfterCaptcha"])
                        if getrole is not False:
                            await member.add_roles(getrole)
                    except Exception as error:
                        print(f"Give and remove roles failed : {error}")
                    try:
                        getrole = get(member.guild.roles,
                                      id=data["temporaryRole"])
                        await member.remove_roles(getrole)
                    except Exception as error:
                        print(f"No temp role found (onJoin) : {error}")
                    time.sleep(3)
                    await captchaEmbed.delete()
                    await msg.delete()
                    # Logs
                    embed = discord.Embed(
                        title=f"**{member} が認証に成功しました**", description=f"**__ユーザー情報 :__**\n\n**名前 :** {member}\n**ID :** {member.id}", color=0x2fa737)
                    embed.set_footer(text=f"at {memberTime}")
                    await sendLogMessage(self, event=member, channel=logChannel, embed=embed)

                else:
                    link = await captchaChannel.create_invite()  # Create an invite
                    embed = discord.Embed(
                        description=f"{member.mention} failed the captcha.", color=0xca1616)  # Red
                    await captchaChannel.send(embed=embed, delete_after=5)
                    embed = discord.Embed(title=f"**あなたは {member.guild.name} からキックされました**",
                                          description=f"理由 : 認証に失敗しました\nサーバーリンク : <{link}>", color=0xff0000)
                    await member.send(embed=embed)
                    await member.kick()  # Kick the user
                    time.sleep(3)
                    await captchaEmbed.delete()
                    await msg.delete()
                    # Logs
                    embed = discord.Embed(
                        title=f"**{member} がキックされました**", description=f"**理由 :** 認証に失敗しました\n\n**__ユーザー情報 :__**\n\n**名前 :** {member}\n**ID :** {member.id}", color=0xff0000)
                    embed.set_footer(text=f"at {memberTime}")
                    await sendLogMessage(self, event=member, channel=logChannel, embed=embed)

            except (asyncio.TimeoutError):
                link = await captchaChannel.create_invite()  # Create an invite
                embed = discord.Embed(
                    title=f"**時間切れです！**", description=f"{member.mention} 120秒以内に認証しませんでした", color=0xff0000)
                await captchaChannel.send(embed=embed, delete_after=5)
                try:
                    embed = discord.Embed(title=f"**あなたは {member.guild.name} からキックされました**",
                                          description=f"理由 : あなたは120秒以内に認証することができませんでした。\nサーバーリンク : <{link}>", color=0xff0000)
                    await member.send(embed=embed)
                    await member.kick()  # Kick the user
                except Exception as error:
                    print(f"Log failed (onJoin) : {error}")
                time.sleep(3)
                await captchaEmbed.delete()
                # Logs
                embed = discord.Embed(
                    title=f"**{member} がキックされました**", description=f"**理由 :** 120秒以内に認証しませんでした。\n\n**__ユーザー情報 :__**\n\n**名前 :** {member}\n**ID :** {member.id}", color=0xff0000)
                embed.set_footer(text=f"at {memberTime}")
                await sendLogMessage(self, event=member, channel=logChannel, embed=embed)

# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.add_cog(OnJoinCog(bot))
