import json
import math
from collections import Counter

# scryfall card dump filtered to only cards we expect enchant worldle to use
with open("useful-cards.json", "r", encoding="utf8") as mtgfile:
    mtgjson = mtgfile.read()

allcards = json.loads(mtgjson)

with open("patterns.json", "r", encoding="utf8") as patfile:
    patjson = patfile.read()

patterns = json.loads(patjson)

total_patterns = len(allcards)

def report(index, name):
    if index % 1000 == 0:
        print(f"Processed {index} cards. Last card: {name}")

def calc_entropy(card,i):
    report(i,card["name"])
    patterns = [patterns[(card,answer)] for answer in allcards]
    counts = Counter(patterns)
    probabilities = {pattern: counts[pattern] / total_patterns for pattern in counts}
    informations = {pattern: math.log2(1/probabilities[pattern]) for pattern in probabilities}
    terms = [probabilities[pattern] * informations[pattern] for pattern in counts]
    entropy = sum(terms)
    return entropy

entropies = [{"name": card["name"], "ent": calc_entropy(card,i)} for i,card in enumerate(allcards)]

outjson = json.dumps(entropies,indent=4)

with open("entropies.json", "w", encoding="utf8") as outfile:
    outfile.write(outjson)