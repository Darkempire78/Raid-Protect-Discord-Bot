import discord

from discord.ext import commands

# ------------------------ COGS ------------------------ #


class HelpCog(commands.Cog, name="ヘルプコマンド"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #

    @commands.command(name='help',
                      usage="(コマンド名)",
                      description="ヘルプを表示します。")
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def help(self, ctx, commandName=None):

        commandName2 = None
        stop = False

        if commandName is not None:
            for i in self.bot.commands:
                if i.name == commandName.lower():
                    commandName2 = i
                    break
                else:
                    for j in i.aliases:
                        if j == commandName.lower():
                            commandName2 = i
                            stop = True
                            break
                if stop:
                    break

            if commandName2 is None:
                await ctx.channel.send("コマンドが見つかりません！")
            else:
                embed = discord.Embed(title=f"**{commandName2.name.upper()} コマンド :**",
                                      description="[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)", color=0xdeaa0c)
                embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
                embed.add_field(name=f"**コマンド名 :**",
                                value=f"{commandName2.name}", inline=False)
                aliases = ""
                if len(commandName2.aliases) > 0:
                    for aliase in commandName2.aliases:
                        aliases = aliase
                else:
                    commandName2.aliases = None
                    aliases = None
                embed.add_field(name=f"**別名 :**",
                                value=f"{aliases}", inline=False)
                if commandName2.usage is None:
                    commandName2.usage = ""
                embed.add_field(
                    name=f"**使い方 :**", value=f"{self.bot.command_prefix}{commandName2.name} {commandName2.usage}", inline=False)
                embed.add_field(
                    name=f"**説明 :**", value=f"{commandName2.description}", inline=False)
                embed.set_footer(text="Bot Created by Darkempire#8245")
                await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=f"__**{self.bot.user.name.upper()}のヘルプ**__",
                                  description="[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)", color=0xdeaa0c)
            embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
            embed.add_field(name=f"__コマンド :__", value=f"**{self.bot.command_prefix}help (コマンド名) :**指定したコマンドのヘルプを表示します\n\n**{self.bot.command_prefix}setup <on/off> :** Captcha保護の設定をします\n**{self.bot.command_prefix}settings :** 設定一覧を表示します\n**{self.bot.command_prefix}giveroleaftercaptcha <ロールID/off> :** Captcha認証後にユーザーにロールを与えるか設定します\n**{self.bot.command_prefix}minaccountage <数字 (1時間単位)> :** アカウントを作成して何時間後の人が参加できるか設定します (デフォルトでは24時間です).\n**{self.bot.command_prefix}antinudity <true/false> :** わいせつな写真からの保護をするかどうか設定します\n**{self.bot.command_prefix}antiprofanity <true/false> :** 汚い言葉を使った発言からの保護をするかどうか設定します\n**{self.bot.command_prefix}antispam <true/false> :** スパム保護をするかどうか設定します\n**{self.bot.command_prefix}allowspam <#channel> (remove) :** 指定したチャンネルのスパム許可・禁止を設定します\n**{self.bot.command_prefix}lock | unlock <#channel/ID> :** チャンネルのロックを設定・解除します\n\n**{self.bot.command_prefix}userinfos <@user/ID> :** ユーザーの情報を表示します", inline=False)
            embed.set_footer(text="Bot Created by Darkempire#8245")
            await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))
