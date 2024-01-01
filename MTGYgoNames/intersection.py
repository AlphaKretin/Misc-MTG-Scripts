import json

with open("oracle-cards-20230823210155.json", "r", encoding="utf8") as mtgfile:
    mtgjson = mtgfile.read()

with open("cardinfo.php.json", "r", encoding="utf8") as ygofile:
    ygojson = ygofile.read()

mtgobj = json.loads(mtgjson)
ygoobj = json.loads(ygojson)


def trim_name(name):
    removespecial = "".join(e for e in name if e.isalnum())
    return removespecial.lower()


mtgnames = [trim_name(card["name"]) for card in mtgobj]
ygonames = [trim_name(card["name"]) for card in ygoobj["data"]]

intnames = list(set(mtgnames).intersection(ygonames))

print(len(intnames))

out = "\n".join(intnames)

with open("sharednames.txt", "w", encoding="utf8") as outfile:
    outfile.write(out)
