![](https://img.shields.io/codefactor/grade/github/Darkempire78/Raid-Protect-Discord-Bot?style=for-the-badge) 
![](https://img.shields.io/github/repo-size/Darkempire78/Raid-Protect-Discord-Bot?style=for-the-badge) 
![](https://img.shields.io/badge/SOURCERY-ENABLED-green?style=for-the-badge) <a href="https://discord.com/invite/sPvJmY7mcV"><img src="https://img.shields.io/discord/831524351311609907?color=%237289DA&label=DISCORD&style=for-the-badge"></a>

# THIS REPO IS DEPRECATED
## Modules may/will not work, and no support will be given on discord and/or git issues
## If you still want to contribute to this project, feel free to update it and make a pull request, it will still be read.

# Raid Protect Discord Bot

Raid Protect is a Discord bot wich allow to protect your discord server efficiently.

## Captcha
![](https://github.com/Darkempire78/Raid-Protect-Discord-Bot/blob/master/Capture1.PNG)

## Installation

Install all dependencies:

* `pip install -r requirements.txt`
* Then put your Discord token that can be found in the Discord's developers portal inside `config.example.json` (do not change anything else)
* Rename it to `config.json`
* This bot have to use the "server members intent", so you have to enable it in the Discord's developers portal

Finally, host the bot and invite it to your own server.

## Features

This Discord Bot protect your Discord server with many functions.

* Captcha firewall
* Minimum account age required
* Anti nudity image
* Anti profanity
* Anti spam
* Logs
* Basic moderation commands
* Multi guild support
* Multi language (EN, FR)

Restrictions do not affect members with ADMINISTRATOR permission !

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
?allowspam <#channel> (False) : Enable or disable the spam protection in a specific channel.
?lock | unlock <#channel> : Lock/Unlock a specific channel.

?userinfos <@user/ID> : Get user infomations.

?ban <@user/ID> : Ban the user.
?kick <@user/ID> : Kick the user.

?changeprefix <prefix> : Change the bot's prefix for the guild.
?changelanguage <language> : Change the bot's language for the guild.
?help : display help.
```

## Potential errors

### ImportError: cannot import name 'joblib' form 'sklearn.externals'
You have to download the last version of profanity_check.
Unstall you current version and download the v1.0.6 with `git+https://github.com/dimitrismistriotis/profanity-check` 

## Discord

Join the Discord server !

### - Deprecated Note : No support will be given for this repo, feel free to join it if you just want to hang with other fellow contributors and devs -
[![](https://i.imgur.com/UfyvtOL.png)](https://discord.gg/sPvJmY7mcV)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License

This project is under [GPLv3](https://github.com/Darkempire78/Raid-Protect-Discord-Bot/blob/master/LICENSE).

## Stargazers
[![Stargazers over time](https://starchart.cc/Darkempire78/Raid-Protect-Discord-Bot.svg)](https://starchart.cc/Darkempire78/Raid-Protect-Discord-Bot)

# Advice :

You should use [Discord Tools](https://marketplace.visualstudio.com/items?itemName=Darkempire78.discord-tools) to code your Discord bots on Visual Studio Code easier.
Works for Python (Discord.py), Javascript (Discord.js, Eris) and Java (JDA). Generate template bot and code (snippets).
- **Download :** https://marketplace.visualstudio.com/items?itemName=Darkempire78.discord-tools
- **Repository :** https://github.com/Darkempire78/Discord-Tools
