import json

with open("cardinfo.php.json", "r", encoding="utf8") as ygofile:
    ygojson = ygofile.read()

ygoobj = json.loads(ygojson)


def trim_name(name):
    removespecial = "".join(e for e in name if e.isalnum())
    return removespecial.lower()


ygonames = [trim_name(card["name"]) for card in ygoobj["data"]]

ygonames.sort(key=len, reverse=True)

print(ygonames[0])

out = "\n".join(ygonames[0:10])

with open("longnames.txt", "w", encoding="utf8") as outfile:
    outfile.write(out)
