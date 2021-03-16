import json

import discord
from discord.ext import commands
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
    async def give_role_after_captcha(self, ctx, role_id):

        try:
            role_id = int(role_id)
            with open("configuration.json", "r") as config:
                data = json.load(config)
                data["roleGivenAfterCaptcha"] = role_id
                new_data = json.dumps(data, indent=4, ensure_ascii=False)

            with open("configuration.json", "w") as config:
                config.write(new_data)

            embed = discord.Embed(
                title=f"**成功**", description=f"今後 <@&{role_id}> が認証後、ユーザーに与えられます。", color=0x2fa737)  # Green
            await ctx.channel.send(embed=embed)

        except Exception as error:
            print(f"giveroleaftercaptcha error : {error}")
            role_id = role_id.lower()
            if role_id == "off":
                with open("configuration.json", "r") as config:
                    data = json.load(config)
                    data["roleGivenAfterCaptcha"] = False
                    new_data = json.dumps(data, indent=4, ensure_ascii=False)
                with open("configuration.json", "w") as config:
                    config.write(new_data)

            else:
                embed = discord.Embed(
                    title=f"**エラー**", description=f"引数は`ロールID`か`off`を指定してください\n"
                                                  f"例 : ``{self.bot.command_prefix}giveroleaftercaptcha <ロールID/off>``",
                    color=0xff0000)
                await ctx.channel.send(embed=embed)


# ------------------------ BOT ------------------------ #

def setup(bot):
    bot.add_cog(GiveRoleAfterCaptchaCog(bot))
