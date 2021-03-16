![](https://img.shields.io/codefactor/grade/github/Darkempire78/Raid-Protect-Discord-Bot?style=for-the-badge) 
![](https://img.shields.io/github/repo-size/Darkempire78/Raid-Protect-Discord-Bot?style=for-the-badge) 
![](https://img.shields.io/badge/SOURCERY-ENABLED-green?style=for-the-badge)

[:jp: Japan Version](https://github.com/Alpaca131/Raid-Protect-Discord-Bot-JP_translated)

# Raid Protect Discord Bot

Raid Protect is a Discord bot wich allow to protect your discord server efficiently.

## Captcha
![](https://github.com/Darkempire78/Raid-Protect-Discord-Bot/blob/master/Capture1.PNG)

## Installation

Install all dependencies:

```bash
pip install -r requirements.txt
```
Then put your Discord token that can be found in the Discord's developers portal inside `configuration.json`.
This bot have to use the "server members intent", so you have to enable it in the Discord's developers portal.

Finally, host the bot and invite it to your own server.

## Features

This Discord Bot protect your Discord server with many functions.

* Captcha firewall
* Minimum account age required
* Anti nudity image
* Anti profanity
* Anti spam
* Logs

## Logs

![](https://github.com/Darkempire78/Raid-Protect-Discord-Bot/blob/master/Capture2.PNG)

## Commands

```
?setup <on/off> : Set up the captcha protection.
?settings : Display the list of settings.
?giveroleaftercaptcha <role ID/off> : Give a role after that the user passed the captcha.
?minaccountage <number (hours)> : set a minimum age to join the server (24 hours by default).
?antinudity <true/false> : Enable or disable the nudity image protection.
?antiprofanity <true/false> : Enable or disable the profanity protection.
?antispam <true/false> : Enable or disable the spam protection.
?allowspam <#channel> (remove) : Enable or disable the spam protection in a specific channel.
?lock | unlock <#channel> : Lock/Unlock a specific channel.

?userinfos <@user/ID> : Get user infomations.

?help : display help.
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License

This project is under [GPLv3](https://github.com/Darkempire78/Raid-Protect-Discord-Bot/blob/master/LICENSE).


# Advice :

You should use [Discord Tools](https://marketplace.visualstudio.com/items?itemName=Darkempire78.discord-tools) to code your Discord bots on Visual Studio Code easier.
Works for Python (Discord.py), Javascript (Discord.js) and Java (JDA). Generate template bot and code (snippets).
- **Download :** https://marketplace.visualstudio.com/items?itemName=Darkempire78.discord-tools
- **Repository :** https://github.com/Darkempire78/Discord-Tools
