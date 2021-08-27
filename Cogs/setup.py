import discord
import asyncio
import json
from discord.ext import commands
from discord.utils import get
from Tools.utils import getConfig, updateConfig

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
            embed = discord.Embed(title = f"**ARE YOU SURE DO YOU WANT TO SET UP THE CAPTCHA PROTECTION ?**", description = f"**Set up the captcha protection includes the creation of :**\n\n- captcha verification channel\n- log channel\n- temporary role (before that the captcha was passed)\n\n**If you want to set up the captcha protection write \"__yes__\" else write \"__no__\".**", color = 0xff0000)
            await ctx.channel.send(embed = embed)
            # Ask if user are sure
            def check(message):
                if message.author == ctx.author and message.content in ["yes", "no"]:
                    return message.content

            try:
                msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                if msg.content == "no":
                    await ctx.channel.send("The set up of the captcha protection was abandoned.")
                else:
                    try:
                        loading = await ctx.channel.send("Creation of captcha protection...")

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
                        embed = discord.Embed(title = f"**CAPTCHA WAS SET UP WITH SUCCESS**", description = f"The captcha was set up with success.", color = 0x2fa737) # Green
                        await ctx.channel.send(embed = embed)
                    except Exception as error:
                        embed = discord.Embed(title=f"**ERROR**", description=f"An error was encountered during the set up of the captcha.\n\n**ERROR :** {error}", color=0xe00000) # Red
                        embed.set_footer(text="Bot Created by Darkempire#8245")
                        return await ctx.channel.send(embed=embed)

            
            except (asyncio.TimeoutError):
                embed = discord.Embed(title = f"**TIME IS OUT**", description = f"{ctx.author.mention} has exceeded the response time (30s).", color = 0xff0000)
                await ctx.channel.send(embed = embed)

        elif onOrOff == "off":
            loading = await ctx.channel.send("Deletion of captcha protection...")
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
            embed = discord.Embed(title = f"**CAPTCHA WAS DELETED WITH SUCCESS**", description = f"The captcha was deleted with success.", color = 0x2fa737) # Green
            await ctx.channel.send(embed = embed)
            if len(noDeleted) > 0:
                errors = ", ".join(noDeleted)
                embed = discord.Embed(title = f"**CAPTCHA DELETION ERROR**", description = f"**Error(s) detected during the deletion of the ** ``{errors}``.", color = 0xe00000) # Red
                await ctx.channel.send(embed = embed)


        else:
            embed = discord.Embed(title=f"**ERROR**", description=f"The setup argument must be on or off\nFollow the example : ``{self.bot.command_prefix}setup <on/off>``", color=0xe00000) # Red
            embed.set_footer(text="Bot Created by Darkempire#8245")
            return await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(SetupCog(bot))