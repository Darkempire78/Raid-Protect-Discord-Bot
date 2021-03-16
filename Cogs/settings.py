import json

import discord
from discord.ext import commands


# ------------------------ COGS ------------------------ #

class SettingsCog(commands.Cog, name="設定コマンド"):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------------------------------------ #

    @commands.command(name='settings',
                      description="Display the settings.")
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def settings(self, ctx):

        with open("configuration.json", "r") as config:
            data = json.load(config)
            captcha = data["captcha"]
            captcha_channel = data["captchaChannel"]
            log_channel = data["logChannel"]
            temporary_role = data["temporaryRole"]
            role_given_after_captcha = data["roleGivenAfterCaptcha"]
            min_account_age = data["minAccountDate"]
            antispam = data["antiSpam"]
            allow_spam = data["allowSpam"]
            anti_nudity = data["antiNudity"]
            anti_profanity = data["antiProfanity"]

            min_account_age = int(min_account_age / 3600)

            allow_spam2 = ""
            if len(allow_spam) == 0:
                allow_spam2 = "None"
            else:
                for x in allow_spam:
                    allow_spam2 = f"{allow_spam2}<#{x}>, "

            if role_given_after_captcha is not False:
                role_given_after_captcha = f"<@&{role_given_after_captcha}>"
            if captcha_channel is not False:
                captcha_channel = f"<#{captcha_channel}>"
            if log_channel is not False:
                log_channel = f"<#{log_channel}>"

        embed = discord.Embed(title=f"**サーバー設定**",
                              description=f"[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)",
                              color=0xdeaa0c)
        embed.add_field(name=f"**Captcha保護** - ``({self.bot.command_prefix}setup <on/off>)``",
                        value=f"Captchaの状態 : {captcha}\n"
                              f"Captchaのチャンネル : {captcha_channel}\n"
                              f"Botのログ : {log_channel}\n"
                              f"一時的なロール : <@&{temporary_role}>",
                        inline=False)
        embed.add_field(
            name=f"**Captcha認証後に付与されるロール** - ``({self.bot.command_prefix}giveroleaftercaptcha <role ID/off>)``",
            value=f"Captcha認証後に付与されるロール : **{role_given_after_captcha}**", inline=False)
        embed.add_field(name=f"**アカウントを作成した時間による制限** - ``({self.bot.command_prefix}minaccountage <number (hours)>)``",
                        value=f"最低経過時間 : **{min_account_age} hours**", inline=False)
        embed.add_field(name=f"**アンチスパム** - ``({self.bot.command_prefix}antispam <true/false>)``",
                        value=f"アンチスパムの状態 : **{antispam}**", inline=False)
        embed.add_field(name=f"**スパムの許可** - ``({self.bot.command_prefix}allowspam <#channel> (remove))``",
                        value=f"スパムが許可されているチャンネル : **{allow_spam2[:-2]}**", inline=False)
        embed.add_field(name=f"**わいせつな写真からの保護** - ``({self.bot.command_prefix}antinudity <true/false>)``",
                        value=f"わいせつな写真からの保護状態 : **{anti_nudity}**", inline=False)
        embed.add_field(name=f"**暴言や汚い言葉からの保護** - ``({self.bot.command_prefix}antiprofanity <true/false>)``",
                        value=f"暴言や汚い言葉からの保護状態 : **{anti_profanity}**", inline=False)
        embed.set_footer(text="Bot Created by Darkempire#8245")
        return await ctx.channel.send(embed=embed)


# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(SettingsCog(bot))
