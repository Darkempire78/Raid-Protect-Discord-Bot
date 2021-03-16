import discord
import asyncio
import json

from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions


# ------------------------ COGS ------------------------ #

class SetupCog(commands.Cog, name="セットアップを行うコマンド"):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------------------------------------ #

    # noinspection PyBroadException
    @commands.command(name='setup',
                      aliases=["captcha"],
                      usage="<on/off>",
                      description="Captcha認証を有効または無効にします。")
    @has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    @commands.guild_only()
    async def setup(self, ctx, on_or_off):

        on_or_off = on_or_off.lower()

        if on_or_off == "on":
            embed = discord.Embed(title=f"**本当にCaptcha認証を有効化しますか？**",
                                  description=f"**有効化すると以下を作成します。 :**\n\n"
                                              f"- Captcha認証チャンネル\n"
                                              f"- ログチャンネル\n"
                                              f"- Captcha認証をパスする前の一時的なロール\n\n"
                                              f"**本当に有効化しますか？以下のどちらかを送信して下さい。"
                                              f"\"__yes__\" or \"__no__\".**",
                                  color=0xff0000)
            await ctx.channel.send(embed=embed)

            # Ask if user are sure
            def check(message):
                if message.author == ctx.author and message.content in ["yes", "no"]:
                    return message.content

            try:
                msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                if msg.content == "no":
                    await ctx.channel.send("Captcha認証のセットアップを中止しました。")
                else:
                    try:
                        loading = await ctx.channel.send("Captcha認証を有効化しています…")

                        # Data
                        with open("configuration.json", "r") as config:
                            data = json.load(config)

                        # Create role
                        temporary_role = await ctx.guild.create_role(name="untested")
                        # Hide all channels
                        for channel in ctx.guild.channels:
                            if isinstance(channel, discord.TextChannel):
                                await channel.set_permissions(temporary_role, read_messages=False)
                            elif isinstance(channel, discord.VoiceChannel):
                                await channel.set_permissions(temporary_role, read_messages=False, connect=False)
                        # Create captcha channel
                        captcha_channel = await ctx.guild.create_text_channel('verification')
                        await captcha_channel.set_permissions(temporary_role, read_messages=True, send_messages=True)
                        await captcha_channel.set_permissions(ctx.guild.default_role, read_messages=False)
                        await captcha_channel.edit(slowmode_delay=5)
                        # Create log channel
                        if data["logChannel"] is False:
                            log_channel = await ctx.guild.create_text_channel(f"{self.bot.user.name}-logs")
                            await log_channel.set_permissions(ctx.guild.default_role, read_messages=False)
                            data["logChannel"] = log_channel.id

                        # Edit configuration.json
                        # Add modifications
                        data["captcha"] = True
                        data["temporaryRole"] = temporary_role.id
                        data["captchaChannel"] = captcha_channel.id
                        new_data = json.dumps(data, indent=4, ensure_ascii=False)

                        with open("configuration.json", "w") as config:
                            config.write(new_data)

                        await loading.delete()
                        embed = discord.Embed(title=f"**Captcha認証が正常に有効化されました**",
                                              description=f"Captcha認証が正常に有効化されました。",
                                              color=0x2fa737)  # Green
                        await ctx.channel.send(embed=embed)
                    except Exception as error:
                        embed = discord.Embed(title=f"**ERROR**",
                                              description=f"Captcha認証の有効化中にエラーが発生しました。"
                                                          f"\n\n**ERROR :** {error}",
                                              color=0xe00000)  # Red
                        embed.set_footer(text="Bot Created by Darkempire#8245")
                        return await ctx.channel.send(embed=embed)

            except asyncio.TimeoutError:
                embed = discord.Embed(title=f"**タイムアウト**",
                                      description=f"{ctx.author.mention}30秒以内にメッセージが送信されなかったためタイムアウトしました。",
                                      color=0xff0000)
                await ctx.channel.send(embed=embed)

        elif on_or_off == "off":
            loading = await ctx.channel.send("Captcha認証を無効化中…")
            with open("configuration.json", "r") as config:
                data = json.load(config)
                # Add modifications
                data["captcha"] = False

            # Delete all
            no_deleted = []
            try:
                temporary_role = get(ctx.guild.roles, id=data["temporaryRole"])
                await temporary_role.delete()
            except Exception:
                no_deleted.append("temporaryRole")
            try:
                captcha_channel = self.bot.get_channel(data["captchaChannel"])
                await captcha_channel.delete()
            except Exception:
                no_deleted.append("captchaChannel")

            # Add modifications
            data["captchaChannel"] = False
            new_data = json.dumps(data, indent=4, ensure_ascii=False)
            # Edit configuration.json
            with open("configuration.json", "w") as config:
                config.write(new_data)

            await loading.delete()
            embed = discord.Embed(title=f"**Captcha認証が正常に無効化されました。**",
                                  description=f"The captcha was deleted with success.", color=0x2fa737)  # Green
            await ctx.channel.send(embed=embed)
            if len(no_deleted) > 0:
                errors = ", ".join(no_deleted)
                embed = discord.Embed(title=f"**ERROR**",
                                      description=f"**以下を削除中にエラーが発生しました。** `{errors}`.",
                                      color=0xe00000)  # Red
                await ctx.channel.send(embed=embed)

        else:
            embed = discord.Embed(title=f"**ERROR**",
                                  description=f"コマンドの引数はonかoffである必要があります。\n"
                                              f"例 : `{self.bot.command_prefix}setup <on/off>`",
                                  color=0xe00000)  # Red
            embed.set_footer(text="Bot Created by Darkempire#8245")
            return await ctx.channel.send(embed=embed)


# ------------------------ BOT ------------------------ #

def setup(bot):
    bot.add_cog(SetupCog(bot))
