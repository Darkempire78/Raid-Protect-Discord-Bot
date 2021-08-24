import json

def getConfig():
    with open("config.json", "r") as config:
        data = json.load(config)
    return data

def updateConfig(newData):
    with open("config.json", "w") as config:
        config.write(newData)