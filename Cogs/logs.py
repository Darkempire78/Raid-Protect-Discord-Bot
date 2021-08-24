import discord
import json
from discord.ext import commands
from Tools.utils import getConfig, updateConfig

# ------------------------ COGS ------------------------ #  

class LogsCog(commands.Cog, name="change setting from logs command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'logs', 
                        aliases= ["log", "setlog", "setlogs", "logchannel"],
                        usage="<true/false>",
                        description="Enable or disable the log system.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def logs(self, ctx, logChannel):

        logChannel = logChannel.lower()

        if logChannel == "true":
            # Create channel
            logChannel = await ctx.guild.create_text_channel(f"{self.bot.user.name}-logs")
            await logChannel.set_permissions(ctx.guild.default_role, read_messages=False)

            data = getConfig()
            # Add modifications
            data["logChannel"] = logChannel.id
            newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**LOG CHANNEL WAS ENABLED**", description = f"The log channel was enabled.", color = 0x2fa737) # Green
        else:
            # Read configuration.json
            data = getConfig()

            # Delete
            logChannel = self.bot.get_channel(data["logChannel"])
            await logChannel.delete()

            # Add modifications
            data["logChannel"] = False
            newdata = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title = f"**LOG CHANNEL WAS DISABLED**", description = f"The log channel was disabled.", color = 0xe00000) # Red
        
        await ctx.channel.send(embed = embed)
        
        updateConfig(newdata)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(LogsCog(bot))