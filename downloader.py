import os.path
from urllib.parse import unquote, urlsplit

import requests


def download_image(url, folder):
    """Function for downloading images.
    Args:
        url (str): Link to the image you want to download.
        folder (str): Folder where to save.
    returns:
        str: The path to the file where the picture is saved.
    """
    filename = urlsplit(unquote(url)).path.split("/")[-1]
    picture_path = os.path.join(folder, filename)
    response = requests.get(url)
    response.raise_for_status()
    with open(picture_path, "wb") as file:
        file.write(response.content)
    return picture_path
