import json

with open("entropies.json", "r", encoding="utf8") as mtgfile:
    entropyjson = mtgfile.read()

entropies = json.loads(entropyjson)

sorted_ents = sorted(entropies, key=lambda d: d["ent"], reverse=True)

print(sorted_ents[0])

outjson = json.dumps(sorted_ents,indent=4)

with open("entropies_sorted.json", "w", encoding="utf8") as outfile:
    outfile.write(outjson)