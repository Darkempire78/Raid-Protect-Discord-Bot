import discord
import json

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class MinAccountAgeCog(commands.Cog, name="change min account age command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'minaccountage', 
                        aliases= ["minage", "agarequired", "age"],
                        usage="<numberInSecond/false>",
                        description="Update or disable the minimal account age to join the server.")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def minaccountage(self, ctx, accountAge):

        accountAge = accountAge.lower()

        if accountAge == "false":
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["minAccountDate"] = False
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            with open("configuration.json", "w") as config:
                config.write(newdata)

            embed = discord.Embed(title = f"**MINIMUM ACCOUNT AGE WAS DISABLED**", description = f"The minimal account age to join the server was disabled.", color = 0x2fa737) # Green
            await ctx.channel.send(embed = embed)
        else:
            try:
                accountAge = int(accountAge)
                # hour to second
                accountAge *= 3600

                # Edit configuration.json
                with open("configuration.json", "r") as config:
                    data = json.load(config)
                    # Add modifications
                    data["minAccountDate"] = accountAge
                    newdata = json.dumps(data, indent=4, ensure_ascii=False)

                with open("configuration.json", "w") as config:
                    config.write(newdata)

                embed = discord.Embed(title = f"**MINIMUM ACCOUNT AGE WAS UPDATED**", description = f"The minimal account age to join the server was updated.", color = 0x2fa737) # Green
                await ctx.channel.send(embed = embed)

            except:
                embed = discord.Embed(title=f"**ERROR**", description=f"The minimum account age must be a number (default = 24 hours)\nFollow the example : ``{self.bot.command_prefix}minaccountage <number (hours)>``", color=0xe00000) # Red
                embed.set_footer(text="Bot Created by Darkempire#8245")
                return await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(MinAccountAgeCog(bot))
