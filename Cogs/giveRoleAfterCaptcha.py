import discord
import json
from Tools.utils import getConfig, updateConfig, getGuildPrefix
from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class GiveRoleAfterCaptchaCog(commands.Cog, name="giveRoleAfterCaptcha command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'giveroleaftercaptcha', 
                        aliases= ["grac", "giverole", "captcharole"],
                        usage="<ID/off>",
                        description="Enable or disable the role given after the captcha.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def giveroleaftercaptcha (self, ctx, roleId):

        try:
            roleId = int(roleId)
            data = getConfig(ctx.guild.id)
            data["roleGivenAfterCaptcha"] = roleId
            

            updateConfig(ctx.guild.id, data)
            
            embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "global", "SUCCESS"), description = self.bot.translate.msg(ctx.guild.id, "giveRoleAfterCaptcha", "ROLE_GIVEN_AFTER_CAPTCHA").format(roleId), color = 0x2fa737) # Green
            await ctx.channel.send(embed = embed)
        
        except Exception as error:
            print(f"giveroleaftercaptcha error : {error}")
            roleId = roleId.lower()
            if roleId == "off":
                data = getConfig(ctx.guild.id)
                data["roleGivenAfterCaptcha"] = False
                
                updateConfig(ctx.guild.id, data)

            else:
                prefix = await getGuildPrefix()
                embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "global", "ERROR"), description = self.bot.translate.msg(ctx.guild.id, "global", "INVALID_ARGUMENT").format(prefix), color = 0xff0000)
                await ctx.channel.send(embed = embed)


# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(GiveRoleAfterCaptchaCog(bot))