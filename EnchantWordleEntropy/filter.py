import json

legal_sets = ["lea", "leb", "arn", "atq", "leg", "drk", "fem", "ice", "hml", "all", "mir", "mgb", "vis", "por", "wth", "tmp", "sth", "exo", "p02", "usg", "ulg", "uds", "s99", "ptk", "mmq", "nem", "pcy", "inv", "pls", "apc", "ody", "tor", "jud", "ons", "lgn", "scg", "8ed", "mrd", "dst", "5dn", "chk", "bok", "sok", "rav", "gpt", "dis", "csp", "tsp", "tsb", "plc", "fut", "lrw", "mor", "shm", "eve", "drb", "ala", "con", "arb", "m10", "hop", "zen", "wwk", "roe", "arc", "m11", "v10", "ddf", "som", "mbs", "nph", "cmd", "m12", "v11", "isd", "dka", "avr", "pc2", "m13", "ddj", "rtr", "gtc", "dgm", "m14", "ddl", "ths", "c13", "bng", "jou", "cns", "m15", "ddn", "ktk", "c14", "frf", "dtk", "ori", "cp3", "ddp", "bfz", "exp", "c15", "ogw", "ddq", "soi", "ema", "emn", "cn2", "kld", "mps", "c16", "aer", "akh", "mp2", "hou", "c17", "xln", "rix", "dom", "bbd", "gs1", "m19", "c18", "grn", "med", "g18", "gnt", "rna", "war", "mh1", "m20", "c19", "eld", "gn2", "sld", "thb", "c20", "iko", "m21", "jmp", "znr", "znc", "mznr", "plist", "cmr", "khm", "khc", "mkhm", "sta", "stx", "c21", "mstx", "mh2", "mmh2", "afr", "afc", "mafr", "mid", "mic", "mmid", "vow", "voc", "mvow", "cc2", "nec", "neo", "mneo", "q07", "snc", "ncc", "msnc", "clb", "mclb", "2x2", "dmu", "dmc", "mdmu", "40k", "gn3", "bro", "bot", "brc", "mbro", "j22", "one", "onc", "mom", "moc", "mat", "ltr", "ltc"]

legal_rarities = ["common", "uncommon", "rare", "mythic"]

with open("default-cards-20240101100417.json", "r", encoding="utf8") as mtgfile:
    mtgjson = mtgfile.read()

allcards = json.loads(mtgjson)
print(f"{len(allcards)} cards loaded.")

firstprints = [card for card in allcards if card["reprint"] == False]
print(f"{len(firstprints)} first prints filtered.")

papercards = [card for card in firstprints if "paper" in card["games"]]
print(f"{len(papercards)} paper-legal cards filtered.")

setcards = [card for card in papercards if card["set"] in legal_sets]
print(f"{len(setcards)} cards in legal sets filtered.")

rarecards = [card for card in setcards if card["rarity"] in legal_rarities]
print(f"{len(rarecards)} cards with legal rarities filtered.")

usednames = []
uniquecards = []
# for loop instead of list comprehension to ensure linearity
for card in rarecards:
    if not (card["name"] in usednames):
        uniquecards.append(card)
        usednames.append(card["name"])
print(f"{len(uniquecards)} cards with unique names filtered.")

outjson = json.dumps(uniquecards,indent=4)

with open("useful-cards.json", "w", encoding="utf8") as outfile:
    outfile.write(outjson)