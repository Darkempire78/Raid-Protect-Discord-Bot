import asyncio
import json
import os
import random
import shutil
import string
import time

import Augmentor
import discord
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from discord.ext import commands
from discord.utils import get

from Tools.logMessage import sendLogMessage


# ------------------------ COGS ------------------------ #


class OnJoinCog(commands.Cog, name="on join"):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------------------------------------ #

    # noinspection PyBroadException
    @commands.Cog.listener()
    async def on_member_join(self, member):

        if member.bot:
            return

        # Read configuration.json
        with open("configuration.json", "r") as config:
            data = json.load(config)
            log_channel = data["logChannel"]
            captcha_channel = self.bot.get_channel(data["captchaChannel"])

        mja_at = self.bot.utc2jst(member.joined_at)
        member_time = f"{mja_at.year}-{mja_at.month}-{mja_at.day} {mja_at.hour}:{mja_at.minute}:{mja_at.second}"

        # Check the user account creation date (1 day by default)
        if data["minAccountDate"] is False:
            user_account_date = member.created_at.timestamp()
            if user_account_date < data["minAccountDate"]:
                min_account_date = data["minAccountDate"] / 3600
                embed = discord.Embed(title=f"**あなたは {member.guild.name} からキックされました**",
                                      description=f"**理由**: **あなたのアカウントは作成後{min_account_date}時間しか経っていないため。**",
                                      color=0xff0000)
                await member.send(embed=embed)
                await member.kick()  # Kick the user
                # Logs
                embed = discord.Embed(
                    title=f"**{member} がキックされました**",
                    description=f"**理由**: **当アカウントは作成後{min_account_date}時間しか経過していないため**\n"
                                f"アカウント作成日時 : {self.bot.utc2jst(member.created_at)}\n\n"
                                f"**__ユーザー情報 :__**\n\n**名前 :** {member}\n**ID :** {member.id}",
                    color=0xff0000)
                embed.set_footer(
                    text=f"at {self.bot.utc2jst(member.joined_at)}")
                await sendLogMessage(self, event=member, channel=log_channel, embed=embed)

        if data["captcha"] is True:

            # Give temporary role
            get_role = get(member.guild.roles, id=data["temporaryRole"])
            await member.add_roles(get_role)

            # Create captcha
            image = np.zeros(shape=(100, 350, 3), dtype=np.uint8)

            # Create image
            image = Image.fromarray(image + 255)  # +255 : black to white

            # Add text
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(font="Tools/arial.ttf", size=60)

            # + string.ascii_lowercase + string.digits
            text = ' '.join(random.choice(string.ascii_uppercase)
                            for _ in range(6))

            # Center the text
            W, H = (350, 100)
            w, h = draw.textsize(text, font=font)
            draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=(90, 90, 90))

            # Save
            member_id = member.id
            folder_path = f"captchaFolder/captcha_{member_id}"
            try:
                os.mkdir(folder_path)
            except Exception:
                if os.path.isdir('captchaFolder') is False:
                    os.mkdir("captchaFolder")
                if os.path.isdir(folder_path) is True:
                    shutil.rmtree(folder_path)
                os.mkdir(folder_path)
            image.save(f"{folder_path}/captcha{member_id}.png")

            # Deform
            p = Augmentor.Pipeline(folder_path)
            p.random_distortion(probability=1, grid_width=4,
                                grid_height=4, magnitude=14)
            p.process()

            # Search file in folder
            path = f"{folder_path}/output"
            files = os.listdir(path)
            captcha_name = [i for i in files if i.endswith('.png')]
            captcha_name = captcha_name[0]

            image = Image.open(f"{folder_path}/output/{captcha_name}")

            # Add line
            width = random.randrange(6, 8)
            co1 = random.randrange(0, 75)
            co3 = random.randrange(275, 350)
            co2 = random.randrange(40, 65)
            co4 = random.randrange(40, 65)
            draw = ImageDraw.Draw(image)
            draw.line([(co1, co2), (co3, co4)], width=width, fill=(90, 90, 90))

            # Add noise
            noise_percentage = 0.25  # 25%

            pixels = image.load()  # create the pixel map
            for i in range(image.size[0]):  # for every pixel:
                for j in range(image.size[1]):
                    rdn = random.random()  # Give a random %
                    if rdn < noise_percentage:
                        pixels[i, j] = (90, 90, 90)

            # Save
            image.save(f"{folder_path}/output/{captcha_name}_2.png")

            # Send captcha
            captcha_file = discord.File(
                f"{folder_path}/output/{captcha_name}_2.png")
            captcha_embed = await captcha_channel.send(f"**サーバーに参加するためには認証してください :**\n{member.mention}, "
                                                       f"認証コードを入力することでサーバーにアクセスできます。",
                                                       file=captcha_file)
            # Remove captcha folder
            try:
                shutil.rmtree(folder_path)
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
                    await captcha_channel.send(embed=embed, delete_after=5)
                    # Give and remove roles
                    try:
                        get_role = get(member.guild.roles,
                                       id=data["roleGivenAfterCaptcha"])
                        if get_role is not False:
                            await member.add_roles(get_role)
                    except Exception as error:
                        print(f"Give and remove roles failed : {error}")
                    try:
                        get_role = get(member.guild.roles,
                                       id=data["temporaryRole"])
                        await member.remove_roles(get_role)
                    except Exception as error:
                        print(f"No temp role found (onJoin) : {error}")
                    time.sleep(3)
                    await captcha_embed.delete()
                    await msg.delete()
                    # Logs
                    embed = discord.Embed(
                        title=f"**{member} が認証に成功しました**",
                        description=f"**__ユーザー情報 :__**\n\n**名前 :** {member}\n**ID :** {member.id}",
                        color=0x2fa737)
                    embed.set_footer(text=f"at {member_time}")
                    await sendLogMessage(self, event=member, channel=log_channel, embed=embed)

                else:
                    link = await captcha_channel.create_invite()  # Create an invite
                    embed = discord.Embed(
                        description=f"{member.mention} failed the captcha.", color=0xca1616)  # Red
                    await captcha_channel.send(embed=embed, delete_after=5)
                    embed = discord.Embed(title=f"**あなたは {member.guild.name} からキックされました**",
                                          description=f"理由 : 認証に失敗しました\nサーバーリンク : <{link}>", color=0xff0000)
                    await member.send(embed=embed)
                    await member.kick()  # Kick the user
                    time.sleep(3)
                    await captcha_embed.delete()
                    await msg.delete()
                    # Logs
                    embed = discord.Embed(
                        title=f"**{member} がキックされました**",
                        description=f"**理由 :** 認証に失敗しました\n\n"
                                    f"**__ユーザー情報 :__**\n\n**名前 :** {member}\n**ID :** {member.id}",
                        color=0xff0000)
                    embed.set_footer(text=f"at {member_time}")
                    await sendLogMessage(self, event=member, channel=log_channel, embed=embed)

            except asyncio.TimeoutError:
                link = await captcha_channel.create_invite()  # Create an invite
                embed = discord.Embed(
                    title=f"**時間切れです！**", description=f"{member.mention} 120秒以内に認証しませんでした", color=0xff0000)
                await captcha_channel.send(embed=embed, delete_after=5)
                try:
                    embed = discord.Embed(title=f"**あなたは {member.guild.name} からキックされました**",
                                          description=f"理由 : あなたは120秒以内に認証することができませんでした。\nサーバーリンク : <{link}>",
                                          color=0xff0000)
                    await member.send(embed=embed)
                    await member.kick()  # Kick the user
                except Exception as error:
                    print(f"Log failed (onJoin) : {error}")
                time.sleep(3)
                await captcha_embed.delete()
                # Logs
                embed = discord.Embed(
                    title=f"**{member} がキックされました**",
                    description=f"**理由 :** 120秒以内に認証しませんでした。\n\n"
                                f"**__ユーザー情報 :__**\n\n**名前 :** {member}\n**ID :** {member.id}",
                    color=0xff0000)
                embed.set_footer(text=f"at {member_time}")
                await sendLogMessage(self, event=member, channel=log_channel, embed=embed)


# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.add_cog(OnJoinCog(bot))
