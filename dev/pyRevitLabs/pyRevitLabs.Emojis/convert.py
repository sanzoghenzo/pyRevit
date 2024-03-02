import re
import json

with open(
    "/home/sanzo/dev/pyRevit/dev/pyRevitLabs/pyRevitLabs.Emojis/emojis.json", "r"
) as source:
    emojis = json.load(source)

ZWJ = "\u200D"
for name, emoji in emojis.items():
    emojis[name] = ZWJ.join(emoji)

with open(
    "/home/sanzo/dev/pyRevit/dev/pyRevitLabs/pyRevitLabs.Emojis/emojisNew.json", "w"
) as dest:
    json.dump(emojis, dest)
