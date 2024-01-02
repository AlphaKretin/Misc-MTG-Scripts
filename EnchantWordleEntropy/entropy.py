import json
import math
import sqlite3
from collections import Counter

# scryfall card dump filtered to only cards we expect enchant worldle to use
with open("useful-cards.json", "r", encoding="utf8") as mtgfile:
    mtgjson = mtgfile.read()

allcards = json.loads(mtgjson)

allnames = [card["name"] for card in allcards]

total_patterns = len(allcards)

dbcon = sqlite3.connect("patterns.db")
dbcur = dbcon.cursor()

def report(index, name):
    if index % 1000 == 0:
        print(f"Processed {index} cards. Last card: {name}")

def calc_entropy(card,i):
    report(i,card["name"])
    pairs = [(card["name"],answer) for answer in allnames]
    patterns = []
    # this is pain
    for pair in pairs:
        res = dbcur.execute("SELECT answer, mv, colour, rarity, suptype, subtype, year FROM patterns WHERE guess = ? AND answer = ?",pair)
        patterns += res.fetchall()
    # filter patterns to only include cards in allcards, in case we're checking a subset for a later guess'
    # there's got to be a better way to work with these tuples...
    patterns = [(pattern[1], pattern[2], pattern[3], pattern[4], pattern[5], pattern[6]) for pattern in patterns if pattern[0] in allnames]
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