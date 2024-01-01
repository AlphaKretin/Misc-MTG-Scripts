import json

with open("useful-cards.json", "r", encoding="utf8") as mtgfile:
    mtgjson = mtgfile.read()

allcards = json.loads(mtgjson)

# if not subtype, get type and supertype
def get_types(card,sub=False):
    type_line = card["type_line"]
    type_halves = type_line.split("\u2014")
    # insert blank subtype if none exists
    if len(type_halves) < 2:
        type_halves.append("")
    type_half = (type_halves[1] if sub else type_halves[0]).strip()
    type_list = type_half.split(" ") # fuck "time lord" it isn't real
    return set(type_list) # set is useful for our purposes later

test_card = [card for card in allcards if card["name"] == "Fresh Meat"][0]
print(test_card)

print(get_types(test_card,False))
print(get_types(test_card,True))