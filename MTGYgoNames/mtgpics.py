import json
import time

import requests


def trim_name(name):
    removespecial = "".join(e for e in name if e.isalnum())
    return removespecial.lower()


def transform_card(card):
    return (
        trim_name(card["name"]),
        card["image_uris"]["normal"] if "image_uris" in card else "",
    )


with open("sharednames.txt", "r", encoding="utf8") as namefile:
    names = namefile.read().splitlines()

with open("oracle-cards-20230823210155.json", "r", encoding="utf8") as mtgfile:
    mtgjson = mtgfile.read()

mtgobj = json.loads(mtgjson)

mtgindex = dict([transform_card(card) for card in mtgobj])

for name in names:
    pic_url = mtgindex[name]
    save_name = "images/" + name + "-m.jpg"

    print("Downloading " + save_name)

    resp = requests.get(pic_url)

    with open(save_name, "wb") as f:
        f.write(resp.content)

    # this is the hackiest possible way to do this but i don't wanna piss off scryfall
    time.sleep(0.1)
