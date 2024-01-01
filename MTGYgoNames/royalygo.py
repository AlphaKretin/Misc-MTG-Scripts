import json

with open("cardinfo.php.json", "r", encoding="utf8") as ygofile:
    ygojson = ygofile.read()

ygoobj = json.loads(ygojson)


def trim_name(name):
    removespecial = "".join(e for e in name if e.isalnum())
    return removespecial.lower()


monsters = [card for card in ygoobj["data"] if "Monster" in card["type"]]

ygonames = [trim_name(card["name"]) for card in monsters]

royal_terms = ["king", "queen", "monarch", "lord"]


def is_royal(name):
    for term in royal_terms:
        if term in name:
            return True
    return False


royalnames = [name for name in ygonames if is_royal(name)]

num_royal_names = len(royalnames)

print(num_royal_names)
print(num_royal_names / len(ygonames))

out = "\n".join(royalnames)

with open("royalnames.txt", "w", encoding="utf8") as outfile:
    outfile.write(out)
