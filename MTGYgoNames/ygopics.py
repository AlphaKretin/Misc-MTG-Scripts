import json
import time

import requests


def trim_name(name):
    removespecial = "".join(e for e in name if e.isalnum())
    return removespecial.lower()


def transform_card(card):
    return (
        trim_name(card["name"]),
        card["card_images"][0]["image_url"],
    )


with open("sharednames-rest.txt", "r", encoding="utf8") as namefile:
    names = namefile.read().splitlines()

with open("cardinfo.php.json", "r", encoding="utf8") as ygofile:
    ygojson = ygofile.read()

ygoobj = json.loads(ygojson)

ygoindex = dict([transform_card(card) for card in ygoobj["data"]])

for name in names:
    pic_url = ygoindex[name]
    save_name = "images/" + name + "-y.jpg"

    print("Downloading " + save_name)

    resp = requests.get(pic_url)

    with open(save_name, "wb") as f:
        f.write(resp.content)

    # this is the hackiest possible way to do this but i don't wanna piss off alan
    time.sleep(0.1)
