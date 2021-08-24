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
from PIL import ImageFont, ImageDraw, Image
from Tools.utils import getConfig
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
        data = getConfig(member.guild.id)
        logChannel = data["logChannel"]
        captchaChannel = self.bot.get_channel(data["captchaChannel"])

        memberTime = f"{member.joined_at.year}-{member.joined_at.month}-{member.joined_at.day} {member.joined_at.hour}:{member.joined_at.minute}:{member.joined_at.second}"

        # Check the user account creation date (1 day by default)
        if data["minAccountDate"] is False:
            userAccountDate = member.created_at.timestamp()
            if userAccountDate < data["minAccountDate"]:
                minAccountDate = data["minAccountDate"] / 3600
                embed = discord.Embed(title = f"**YOU HAVE BEEN KICKED FROM {member.guild.name}**", description = f"Reason : Your account is more young that the server limit ({minAccountDate} hours).", color = 0xff0000)
                await member.send(embed = embed)
                await member.kick() # Kick the user
                # Logs
                embed = discord.Embed(title = f"**{member} has been kicked.**", description = f"**Reason :** His account is more young that the server limit ({minAccountDate} hours)\nAccount creation : {member.created_at}\n\n**__User informations :__**\n\n**Name :** {member}\n**Id :** {member.id}", color = 0xff0000)
                embed.set_footer(text= f"at {member.joined_at}")
                await sendLogMessage(self, event=member, channel=logChannel, embed=embed)

        if data["captcha"] is True:
            
            # Give temporary role
            getrole = get(member.guild.roles, id = data["temporaryRole"])
            await member.add_roles(getrole)
            
            # Create captcha
            image = np.zeros(shape= (100, 350, 3), dtype= np.uint8)

            # Create image 
            image = Image.fromarray(image+255) # +255 : black to white

            # Add text
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(font= "Tools/arial.ttf", size= 60)

            text = ' '.join(random.choice(string.ascii_uppercase) for _ in range(6)) # + string.ascii_lowercase + string.digits

            # Center the text
            W, H = (350,100)
            w, h = draw.textsize(text, font= font)
            draw.text(((W-w)/2,(H-h)/2), text, font= font, fill= (90, 90, 90))

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
            p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=14)
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
            draw.line([(co1, co2), (co3, co4)], width= width, fill= (90, 90, 90))
            
            # Add noise
            noisePercentage = 0.25 # 25%

            pixels = image.load() # create the pixel map
            for i in range(image.size[0]): # for every pixel:
                for j in range(image.size[1]):
                    rdn = random.random() # Give a random %
                    if rdn < noisePercentage:
                        pixels[i,j] = (90, 90, 90)

            # Save
            image.save(f"{folderPath}/output/{captchaName}_2.png")

            # Send captcha
            captchaFile = discord.File(f"{folderPath}/output/{captchaName}_2.png")
            captchaEmbed = await captchaChannel.send(f"**YOU MUST PASS THE CAPTCHA TO ENTER IN THE SERVER :**\nPlease {member.mention}, enter the captcha to get access to the whole serveur (only 6 uppercase letters).", file= captchaFile)
            # Remove captcha folder
            try:
                shutil.rmtree(folderPath)
            except Exception as error:
                print(f"Delete captcha file failed {error}")

            # Check if it is the right user
            def check(message):
                if message.author == member and  message.content != "":
                    return message.content

            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check)
                # Check the captcha
                password = text.split(" ")
                password = "".join(password)
                if msg.content == password:

                    embed = discord.Embed(description=f"{member.mention} passed the captcha.", color=0x2fa737) # Green
                    await captchaChannel.send(embed = embed, delete_after = 5)
                    # Give and remove roles
                    try:
                        getrole = get(member.guild.roles, id = data["roleGivenAfterCaptcha"])
                        if getrole is not False:
                            await member.add_roles(getrole)
                    except Exception as error:
                        print(f"Give and remove roles failed : {error}")
                    try:
                        getrole = get(member.guild.roles, id = data["temporaryRole"])
                        await member.remove_roles(getrole)
                    except Exception as error:
                        print(f"No temp role found (onJoin) : {error}")
                    time.sleep(3)
                    try:
                        await captchaEmbed.delete()
                    except discord.errors.NotFound:
                        pass
                    try:
                        await msg.delete()
                    except discord.errors.NotFound:
                        pass
                    # Logs
                    embed = discord.Embed(title = f"**{member} passed the captcha.**", description = f"**__User informations :__**\n\n**Name :** {member}\n**Id :** {member.id}", color = 0x2fa737)
                    embed.set_footer(text= f"at {memberTime}")
                    await sendLogMessage(self, event=member, channel=logChannel, embed=embed)

                else:
                    link = await captchaChannel.create_invite(max_age=172800) # Create an invite
                    embed = discord.Embed(description=f"{member.mention} failed the captcha.", color=0xca1616) # Red
                    await captchaChannel.send(embed = embed, delete_after = 5)
                    embed = discord.Embed(title = f"**YOU HAVE BEEN KICKED FROM {member.guild.name}**", description = f"Reason : You failed the captcha.\nServer link : <{link}>", color = 0xff0000)

                    try:
                        await member.send(embed=embed)
                    except discord.errors.Forbidden:
                        # can't send dm to user
                        pass
                    await member.kick()

                    time.sleep(3)
                    try:
                        await captchaEmbed.delete()
                    except discord.errors.NotFound:
                        pass
                    try:
                        await msg.delete()
                    except discord.errors.NotFound:
                        pass
                    # Logs
                    embed = discord.Embed(title = f"**{member} has been kicked.**", description = f"**Reason :** He failed the captcha.\n\n**__User informations :__**\n\n**Name :** {member}\n**Id :** {member.id}", color = 0xff0000)
                    embed.set_footer(text= f"at {memberTime}")
                    await sendLogMessage(self, event=member, channel=logChannel, embed=embed)

            except (asyncio.TimeoutError):
                link = await captchaChannel.create_invite(max_age=172800) # Create an invite
                embed = discord.Embed(title = f"**TIME IS OUT**", description = f"{member.mention} has exceeded the response time (120s).", color = 0xff0000)
                await captchaChannel.send(embed = embed, delete_after = 5)
                try:
                    embed = discord.Embed(title = f"**YOU HAVE BEEN KICKED FROM {member.guild.name}**", description = f"Reason : You exceeded the captcha response time (120s).\nServer link : <{link}>", color = 0xff0000)
                    await member.send(embed = embed)
                    await member.kick() # Kick the user
                except Exception as error:
                    print(f"Log failed (onJoin) : {error}")
                time.sleep(3)
                await captchaEmbed.delete()
                # Logs
                embed = discord.Embed(title = f"**{member} has been kicked.**", description = f"**Reason :** He exceeded the captcha response time (120s).\n\n**__User informations :__**\n\n**Name :** {member}\n**Id :** {member.id}", color = 0xff0000)
                embed.set_footer(text= f"at {memberTime}")
                await sendLogMessage(self, event=member, channel=logChannel, embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(OnJoinCog(bot))