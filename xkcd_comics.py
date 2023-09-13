import random

import requests


def get_comics():
    """ Func to receive a random comics. """
    last_comics_num = 2825
    comics_num = random.randint(1, last_comics_num)
    response = requests.get(f"https://xkcd.com/{comics_num}/info.0.json")
    response.raise_for_status()
    comics_description = response.json()
    transcript = comics_description["alt"]
    picture_url = comics_description["img"]
    return picture_url, transcript
