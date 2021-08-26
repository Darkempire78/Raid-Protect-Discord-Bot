import os
import json
from Tools.utils import getConfig

class Translate:
    def __init__(self):
        self.translation = {}
        for filename in os.listdir("Languages"):
            if filename.endswith(".json"):
                self.translation[filename[:-5]] = json.load(open(f"Languages/{filename}", "r", encoding="utf-8"))

    def msg(self, guildID, command, message):
        config = getConfig(guildID)
        language = config["language"]
        try:
            return self.translation[language][command][message]
        except:
            # If it's not translated
            return self.translation["en-US"][command][message]