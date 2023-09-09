import random

import requests


def get_comics():
    """ Func to receive a random comics. """
    the_last_comics_no = 2825
    comics_no = random.randint(1, the_last_comics_no)
    response = requests.get(f"https://xkcd.com/{comics_no}/info.0.json")
    response.raise_for_status()
    comics_description = response.json()
    transcript = comics_description["alt"]
    picture_url = comics_description["img"]
    return picture_url, transcript
