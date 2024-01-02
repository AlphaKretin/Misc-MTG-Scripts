import json
import math
import re
import unicodedata
from collections import Counter

# scryfall card dump filtered to only cards we expect enchant worldle to use
with open("useful-cards.json", "r", encoding="utf8") as mtgfile:
    mtgjson = mtgfile.read()

allcards = json.loads(mtgjson)

allnames = [card["name"] for card in allcards]

total_patterns = len(allcards)

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def report(index, name):
    if index % 1 == 0:
        print(f"Processed {index} cards. Last card: {name}")

def calc_entropy(card,i):
    report(i,card["name"])
    with open(f"patterns/{slugify(card['name'])}.json", "r", encoding="utf8") as patfile:
        patjson = patfile.read()
    patterns = json.loads(patjson)
    # filter patterns to only include cards in allcards, in case we're checking a subset for a later guess
    # there's got to be a better way to convert lists to tuples...
    patterns = [(pattern[0], pattern[1], pattern[2], pattern[3], pattern[4], pattern[5]) for answer, pattern in patterns.items() if answer in allnames]
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