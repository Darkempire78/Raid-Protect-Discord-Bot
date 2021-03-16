![](https://img.shields.io/codefactor/grade/github/Alpaca131/Raid-Protect-Discord-Bot-JP_translated?style=for-the-badge) 
![](https://img.shields.io/github/repo-size/Alpaca131/Raid-Protect-Discord-Bot-JP_translated?style=for-the-badge) 
![](https://img.shields.io/badge/SOURCERY-ENABLED-green?style=for-the-badge)

# Raid Protect Discord Bot

Raid Protect は、あなたのDiscordサーバーを効率的に保護することができるDiscordボットです。

もともとは英語だったものを日本語に翻訳して使いやすくしたボットです。

## Captcha
![image](https://github.com/Alpaca131/Raid-Protect-Discord-Bot-JP_translated/blob/master/Capture1.PNG)

## Installation

すべての依存関係をインストールする:

```bash
pip install -r requirements.txt
```
そして、Discordの開発者ポータルにあるトークンを`configuration.json`に入れます。
このボットは、"Member Intent"を使用しなければならないので、Discordの開発者ポータルで有効にする必要があります。

最後に、ボットをあなたのサーバーへ招待します。

## Features

このDiscordボットは、多くの機能であなたのDiscordサーバーを保護します。

* Captcha ファイアウォール
* アカウント作成経過時間に基づく参加制限
* わいせつな画像からの保護
* 暴言などからの保護
* アンチスパム
* ログ

## Logs

![image](https://github.com/Alpaca131/Raid-Protect-Discord-Bot-JP_translated/blob/master/Capture2.PNG)

## Commands

```
?setup <on/off> : キャプチャ保護の設定を行います。
?settings : 設定の一覧を表示します。
?giveroleaftercaptcha <ロールID/off> : ユーザーがcaptchaを通過した後のロールを与えます。
?minaccountage <数字 (1時間単位)> : サーバーに参加するための最低年齢を設定します（デフォルトでは24時間）。
?antinudity <true/false> : わいせつな画像からの保護を有効または無効にします。
?antiprofanity <true/false> : 暴言や汚い言葉からの保護を有効または無効にします。
?antispam <true/false> : スパム防止機能を有効または無効にします。
?allowspam <#channel> (remove) : 特定のチャンネルのスパム保護を有効または無効にします。
?lock | unlock <#channel> : 特定のチャンネルをロック/アンロックします。

?userinfos <@user/ID> : ユーザー情報を取得します。

?help : ヘルプを表示します。
```

## Contributing

プルリクエストを歓迎します。

大きな変更の場合は、まずissueを開いて、変更したい内容について話し合ってください。

## License

このプロジェクトは、親リポジトリの[GPLv3](https://github.com/Alpaca131/Raid-Protect-Discord-Bot-JP_translated/blob/master/LICENSE)ライセンスに基づいています。


# Advice :

[Discord Tools](https://marketplace.visualstudio.com/items?itemName=Darkempire78.discord-tools)を使うと、Visual Studio Code上でのDiscordボットのコーディングが楽になります。
Python(Discord.py)、Javascript(Discord.js)、Java(JDA)で動作します。ひな形ボットとコード（スニペット）を生成します。
- **ダウンロード :** https://marketplace.visualstudio.com/items?itemName=Darkempire78.discord-tools
- **リポジトリ :** https://github.com/Darkempire78/Discord-Tools
