import json

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


# ------------------------ COGS ------------------------ #

class AntiProfanityCog(commands.Cog, name="暴言や汚い言葉からの保護の設定を変更します。"):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------------------------------------ #

    @commands.command(name='antiprofanity',
                      aliases=["profanity"],
                      usage="<true/false>",
                      description="暴言や汚い言葉からの保護を有効または無効にします。")
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def anti_profanity(self, ctx, anti_profanity):

        anti_profanity = anti_profanity.lower()

        if anti_profanity == "true":
            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["antiProfanity"] = True
                new_data = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title="**暴言や汚い言葉からの保護が有効になりました**",
                                  description="暴言や汚い言葉からの保護が有効になりました。", color=0x2fa737)  # Green
        else:
            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["antiProfanity"] = False
                new_data = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(title="**暴言や汚い言葉からの保護が無効になりました**",
                                  description="暴言や汚い言葉からの保護が無効になりました。", color=0xe00000)  # Red

        await ctx.channel.send(embed=embed)

        with open("configuration.json", "w") as config:
            config.write(new_data)


# ------------------------ BOT ------------------------ #

def setup(bot):
    bot.add_cog(AntiProfanityCog(bot))
