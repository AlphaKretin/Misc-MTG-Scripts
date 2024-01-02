import json

# scryfall card dump filtered to only cards we expect enchant worldle to use
with open("useful-cards.json", "r", encoding="utf8") as mtgfile:
    mtgjson = mtgfile.read()

allcards = json.loads(mtgjson)

mines = [card for card in allcards if card["name"] == "Urza's Mine"]

outjson = json.dumps(mines,indent=4)

with open("mines.json", "w", encoding="utf8") as outfile:
    outfile.write(outjson)