import json

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


# ------------------------ COGS ------------------------ #


class AntiNudityCog(commands.Cog, name="わいせつな写真から保護します"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #

    @commands.command(name='antinudity',
                      aliases=["nudity", "porn"],
                      usage="<true/false>",
                      description="わいせつな写真を許可・禁止する設定をします。")
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def anti_nudity(self, ctx, anti_nudity):

        anti_nudity = anti_nudity.lower()

        if anti_nudity == "true":
            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["antiNudity"] = True
                new_data = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(
                title=f"**保護が有効になりました**", description=f"わいせつな写真からの保護をする設定にしました。", color=0x2fa737)  # Green
        else:
            # Edit configuration.json
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["antiNudity"] = False
                new_data = json.dumps(data, indent=4, ensure_ascii=False)

            embed = discord.Embed(
                title=f"**保護が無効になりました**", description=f"わいせつな写真からの保護をしない設定にしました。", color=0xe00000)  # Red

        await ctx.channel.send(embed=embed)

        with open("configuration.json", "w") as config:
            config.write(new_data)

# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.add_cog(AntiNudityCog(bot))
