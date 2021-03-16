import discord
import asyncio
import json

from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions

# ------------------------ COGS ------------------------ #


class GiveRoleAfterCaptchaCog(commands.Cog, name="giveRoleAfterCaptchaコマンド"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #

    @commands.command(name='giveroleaftercaptcha',
                      aliases=["grac", "giverole", "captcharole"],
                      usage="<ロールID/off>",
                      description="Captcha認証後にロールを与える設定をします。")
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def giveroleaftercaptcha(self, ctx, roleId):

        try:
            roleId = int(roleId)
            with open("configuration.json", "r") as config:
                data = json.load(config)
                data["roleGivenAfterCaptcha"] = roleId
                newdata = json.dumps(data, indent=4, ensure_ascii=False)

            with open("configuration.json", "w") as config:
                config.write(newdata)

            embed = discord.Embed(
                title=f"**成功**", description=f"今後 <@&{roleId}> が認証後、ユーザーに与えられます。", color=0x2fa737)  # Green
            await ctx.channel.send(embed=embed)

        except Exception as error:
            print(f"giveroleaftercaptcha error : {error}")
            roleId = roleId.lower()
            if roleId == "off":
                with open("configuration.json", "r") as config:
                    data = json.load(config)
                    data["roleGivenAfterCaptcha"] = False
                    newdata = json.dumps(data, indent=4, ensure_ascii=False)
                with open("configuration.json", "w") as config:
                    config.write(newdata)

            else:
                embed = discord.Embed(
                    title=f"**エラー**", description=f"引数は`ロールID`か`off`を指定してください\n例 : ``{self.bot.command_prefix}giveroleaftercaptcha <ロールID/off>``", color=0xff0000)
                await ctx.channel.send(embed=embed)


# ------------------------ BOT ------------------------ #

def setup(bot):
    bot.add_cog(GiveRoleAfterCaptchaCog(bot))
