import discord
import os
import shutil

from discord.ext import commands
from discord.utils import get


# ------------------------ COGS ------------------------ #  

class OnRemoveCog(commands.Cog, name="on remove"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        if (member.bot):
            return
        
        # Remove user captcha folder
        ID = member.id
        folderPath = f"captchaFolder/captcha_{ID}"
        shutil.rmtree(folderPath) # Remove file

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(OnRemoveCog(bot))

