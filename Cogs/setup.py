import discord
import asyncio
import json
from discord.ext import commands
from discord.utils import get
from Tools.utils import getConfig, updateConfig, getGuildPrefix

# ------------------------ COGS ------------------------ #  

class SetupCog(commands.Cog, name="setup command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'setup',
                        aliases=["captcha"],
                        usage="<on/off>",
                        description="Enable or disable the captcha system.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def setup (self, ctx, onOrOff):

        onOrOff = onOrOff.lower()

        if onOrOff == "on":
            embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "setup", "DO_YOU_WANT_TO_SET_UP_THE_CAPTCHA_PROTECTION"), description = self.bot.translate.msg(ctx.guild.id, "setup", "DO_YOU_WANT_TO_SET_UP_THE_CAPTCHA_PROTECTION_DESCRIPTION"), color = 0xff0000)
            await ctx.channel.send(embed = embed)
            # Ask if user are sure
            def check(message):
                if message.author == ctx.author and message.content in ["yes", "no"]:
                    return message.content

            try:
                msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                if msg.content == "no":
                    await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "setup", "SET_UP_ABANDONED"))
                else:
                    try:
                        loading = await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "setup", "CREATION_OF_CAPTCHA_PRETECTION"))

                        # Data
                        data = getConfig(ctx.guild.id)

                        # Create role
                        temporaryRole = await ctx.guild.create_role(name="untested")
                        # Hide all channels
                        for channel in ctx.guild.channels:
                            if isinstance(channel, discord.TextChannel):

                                perms = channel.overwrites_for(temporaryRole)
                                perms.read_messages=False
                                await channel.set_permissions(temporaryRole, overwrite=perms)
                                
                            elif isinstance(channel, discord.VoiceChannel):

                                perms = channel.overwrites_for(temporaryRole)
                                perms.read_messages=False
                                perms.connect=False
                                await channel.set_permissions(temporaryRole, overwrite=perms)

                        # Create captcha channel
                        captchaChannel = await ctx.guild.create_text_channel('verification')

                        perms = captchaChannel.overwrites_for(temporaryRole)
                        perms.read_messages=True
                        perms.send_messages=True
                        await captchaChannel.set_permissions(temporaryRole, overwrite=perms)

                        perms = captchaChannel.overwrites_for(ctx.guild.default_role)
                        perms.read_messages=False
                        await captchaChannel.set_permissions(ctx.guild.default_role, overwrite=perms)

                        await captchaChannel.edit(slowmode_delay= 5)
                        # Create log channel
                        if data["logChannel"] is False:
                            logChannel = await ctx.guild.create_text_channel(f"{self.bot.user.name}-logs")

                            perms = logChannel.overwrites_for(ctx.guild.default_role)
                            perms.read_messages=False
                            await logChannel.set_permissions(ctx.guild.default_role, overwrite=perms)

                            data["logChannel"] = logChannel.id
                        
                        # Edit configuration.json
                        # Add modifications
                        data["captcha"] = True
                        data["temporaryRole"] = temporaryRole.id
                        data["captchaChannel"] = captchaChannel.id
                        

                        updateConfig(ctx.guild.id, data)
                        
                        await loading.delete()
                        embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "setup", "CAPTCHA_WAS_SET_UP_WITH_SUCCESS"), description = self.bot.translate.msg(ctx.guild.id, "setup", "CAPTCHA_WAS_SET_UP_WITH_SUCCESS_DESCRIPTION"), color = 0x2fa737) # Green
                        await ctx.channel.send(embed = embed)
                    except Exception as error:
                        embed = discord.Embed(title=self.bot.translate.msg(ctx.guild.id, "global", "ERROR"), description=self.bot.translate.msg(ctx.guild.id, "global", "ERROR_OCCURED").format(error), color=0xe00000) # Red
                        embed.set_footer(text=self.bot.translate.msg(ctx.guild.id, "global", "BOT_CREATOR"))
                        return await ctx.channel.send(embed=embed)

            
            except (asyncio.TimeoutError):
                embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "setup", "TIME_IS_OUT"), description = self.bot.translate.msg(ctx.guild.id, "setup", "USER_HAS_EXCEEDED_THE_RESPONSE_TIME").format(ctx.author.mention), color = 0xff0000)
                await ctx.channel.send(embed = embed)

        elif onOrOff == "off":
            loading = await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "setup", "DELETION_OF_THE_CAPTCHA_PROETECTION"))
            data = getConfig(ctx.guild.id)
            data["captcha"] = False
            
            # Delete all
            noDeleted = []
            try:
                temporaryRole = get(ctx.guild.roles, id= data["temporaryRole"])
                await temporaryRole.delete()
            except:
                noDeleted.append("temporaryRole")
            try:  
                captchaChannel = self.bot.get_channel(data["captchaChannel"])
                await captchaChannel.delete()
            except:
                noDeleted.append("captchaChannel")

            # Add modifications
            data["captchaChannel"] = False
            
            # Edit configuration.json
            updateConfig(ctx.guild.id, data)
            
            await loading.delete()
            embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "setup", "CAPTCHA_WAS_DELETED_WITH_SUCCESS"), description = self.bot.translate.msg(ctx.guild.id, "setup", "CAPTCHA_WAS_DELETED_WITH_SUCCESS_DESCRIPTION"), color = 0x2fa737) # Green
            await ctx.channel.send(embed = embed)
            if len(noDeleted) > 0:
                errors = ", ".join(noDeleted)
                prefix = getGuildPrefix()
                embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "setup", "CAPTCHA_DELETION_ERROR"), description = self.bot.translate.msg(ctx.guild.id, "setup", "CAPTCHA_DELETION_ERROR_DESCRIPTION").format(errors), color = 0xe00000) # Red
                await ctx.channel.send(embed = embed)

        else:
            embed = discord.Embed(title=self.bot.translate.msg(ctx.guild.id, "global", "ERROR"), description= self.bot.translate.msg(ctx.guild.id, "setup", "INVALID_ARGUMENT").format(prefix), color=0xe00000) # Red
            embed.set_footer(text=self.bot.translate.msg(ctx.guild.id, "gloval", "BOT_CREATOR"))
            return await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(SetupCog(bot))