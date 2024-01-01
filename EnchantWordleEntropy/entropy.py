import json
import math
from collections import Counter

# scryfall card dump filtered to only cards we expect enchant worldle to use
with open("useful-cards.json", "r", encoding="utf8") as mtgfile:
    mtgjson = mtgfile.read()

allcards = json.loads(mtgjson)

def compare_mv(guess,answer):
    guess_mv = guess["cmc"]
    ans_mv = answer["cmc"]
    if guess_mv == ans_mv:
        return "g" # representing a green square
    if guess_mv > ans_mv:
        if guess_mv - ans_mv <= 2:
            return "ydn" # yellow up arrow
        return "dn"
    # else lesser
    if ans_mv - guess_mv <= 2:
        return "yup"
    return "up"

def compare_colour(guess,answer):
    guess_col = set(guess["color_identity"])
    ans_col = set(answer["color_identity"])
    if guess_col == ans_col:
        return -1 # arbitrary value indicating exact match, otherwise count number of shared colours
    return len(guess_col & ans_col)

ordered_rarities = ["common", "uncommon", "rare", "mythic"]

def compare_rarity(guess,answer):
    guess_rar = ordered_rarities.index(guess["rarity"])
    ans_rar = ordered_rarities.index(answer["rarity"])
    if guess_rar > ans_rar:
        return "dn"
    if guess_rar < ans_rar:
        return "up"
    return "g"

# if not subtype, get type and supertype
def get_types(card,sub=False):
    type_line = card["type_line"]
    type_halves = type_line.split("\u2014")
    # insert blank subtype if none exists - a bit hacky but should be functionally identical to returning the empty set
    # which we could just do here by checking the sub bool but i didn't think about that and the code is 3000 cards deep as of writing
    if len(type_halves) < 2:
        type_halves.append("")
    type_half = (type_halves[1] if sub else type_halves[0]).strip()
    type_list = type_half.split(" ") # fuck "time lord" it isn't real
    return set(type_list) # set is useful for our purposes later

def compare_type(guess,answer,sub=False):
    guess_types = get_types(guess,sub)
    ans_types = get_types(answer,sub)
    if guess_types == ans_types:
        return -1
    return len(guess_types & ans_types)

# we could fuck with datetime but the format is simple enough
def get_year(card):
    date_string = card["released_at"]
    year_string = date_string[0:4] #YYYY-MM-DD
    return int(year_string)

set_order = ["lea", "leb", "arn", "atq", "leg", "drk", "fem", "ice", "hml", "all", "mir", "mgb", "vis", "por", "wth", "tmp", "sth", "exo", "p02", "usg", "ulg", "uds", "s99", "ptk", "mmq", "nem", "pcy", "inv", "pls", "apc", "ody", "tor", "jud", "ons", "lgn", "scg", "8ed", "mrd", "dst", "5dn", "chk", "bok", "sok", "rav", "gpt", "dis", "csp", "tsp", "tsb", "plc", "fut", "lrw", "mor", "shm", "eve", "drb", "ala", "con", "arb", "m10", "hop", "zen", "wwk", "roe", "arc", "m11", "v10", "ddf", "som", "mbs", "nph", "cmd", "m12", "v11", "isd", "dka", "avr", "pc2", "m13", "ddj", "rtr", "gtc", "dgm", "m14", "ddl", "ths", "c13", "bng", "jou", "cns", "m15", "ddn", "ktk", "c14", "frf", "dtk", "ori", "cp3", "ddp", "bfz", "exp", "c15", "ogw", "ddq", "soi", "ema", "emn", "cn2", "kld", "mps", "c16", "aer", "akh", "mp2", "hou", "c17", "xln", "rix", "dom", "bbd", "gs1", "m19", "c18", "grn", "med", "g18", "gnt", "rna", "war", "mh1", "m20", "c19", "eld", "gn2", "sld", "thb", "c20", "iko", "m21", "jmp", "znr", "znc", "mznr", "plist", "cmr", "khm", "khc", "mkhm", "sta", "stx", "c21", "mstx", "mh2", "mmh2", "afr", "afc", "mafr", "mid", "mic", "mmid", "vow", "voc", "mvow", "cc2", "nec", "neo", "mneo", "q07", "snc", "ncc", "msnc", "clb", "mclb", "2x2", "dmu", "dmc", "mdmu", "40k", "gn3", "bro", "bot", "brc", "mbro", "j22", "one", "onc", "mom", "moc", "mat", "ltr", "ltc"]

def compare_set(guess,answer):
    guess_set = guess["set"]
    ans_set = answer["set"]
    if guess_set == ans_set:
        return "g"
    guess_index = set_order.index(guess_set)
    ans_index = set_order.index(ans_set)
    if guess_index > ans_index:
        return "ydn"
    return "yup"

def compare_year(guess,answer):
    guess_yr = get_year(guess)
    ans_yr = get_year(answer)
    if guess_yr > ans_yr:
        return "dn"
    if guess_yr < ans_yr:
        return "up"
    return compare_set(guess,answer)
    

def generate_pattern(guess,answer):
    return (compare_mv(guess,answer),
            compare_colour(guess,answer),
            compare_rarity(guess,answer),
            compare_type(guess,answer,False), # compare type and supertype
            compare_type(guess,answer,True), # compare subtype
            compare_year(guess,answer))

total_patterns = len(allcards)

def report(index, name):
    if index % 1000 == 0:
        print(f"Processed {index} cards. Last card: {name}")

def calc_entropy(card,i):
    report(i,card["name"])
    patterns = [generate_pattern(card,answer) for answer in allcards]
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