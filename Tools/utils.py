import json

def getConfig(guildID):
    with open("config.json", "r") as config:
        data = json.load(config)
    if guildID not in data["guilds"]:
        defaultConfig = {
            "prefix": "?",
            "antiProfanity": True,
            "antiNudity": True,
            "antiSpam": True,
            "allowSpam": [],
            "captcha": False,
            "captchaChannel": False,
            "logChannel": 1,
            "temporaryRole": 1,
            "roleGivenAfterCaptcha": False,
            "minAccountDate": 86400
        }
        updateConfig(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][guildID]

def updateConfig(guildID, data):
    with open("config.json", "r") as config:
        config = json.load(config)
    config["guilds"][guildID] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("config.json", "w") as config:
        config.write(newdata)

async def getGuildPrefix(bot, message):
    # if not message.guild:
    #     
    return "?"
    # else: