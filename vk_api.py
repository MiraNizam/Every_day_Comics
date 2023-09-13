import os
import os.path
from pathlib import Path

import requests
from dotenv import load_dotenv

from downloader import download_image
from xkcd_comics import get_comics


def check_response(response_json):
    if "error" in response_json:
        raise requests.HTTPError(response_json["error"]["error_msg"])


def get_image_server_address(access_token, version, group_id):
    payload = {"group_id": group_id, "access_token": access_token, "v": version}
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    response = requests.get(url, payload)
    response.raise_for_status()
    server_address = response.json()
    check_response(server_address)
    upload_url = server_address["response"]["upload_url"]
    return upload_url


def load_image(upload_url, image_path):
    with open(image_path, 'rb') as file:
        files = {'photo': file}
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    image_location = response.json()
    check_response(image_location)
    server = image_location["server"]
    photo = image_location["photo"]
    image_hash = image_location["hash"]
    return server, photo, image_hash


def save_image(server, photo, image_hash, transcript, access_token, version, group_id):
    payload = {
        "group_id": group_id,
        "photo": photo,
        "server": server,
        "hash": image_hash,
        "caption": transcript,
        "access_token": access_token,
        "v": version,
    }
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    response = requests.post(url, params=payload)
    response.raise_for_status()
    image_description = response.json()
    check_response(image_description)
    owner_id = image_description['response'][0]["owner_id"]
    media_id = image_description['response'][0]["id"]
    text = image_description['response'][0]["text"]
    return owner_id, media_id, text


def publish_image(owner_id, media_id, text, access_token, version, group_owner_id):
    payload = {
        "owner_id": f"-{group_owner_id}",
        "from_group": 1,
        "attachments": f"photo{owner_id}_{media_id}",
        "message": text,
        "access_token": access_token,
        "v": version,
    }
    url = "https://api.vk.com/method/wall.post"
    response = requests.post(url, params=payload)
    response.raise_for_status()
    response_json = response.json()
    check_response(response_json)
    return response_json


def main():
    load_dotenv()
    access_token = os.environ["VK_TOKEN"]
    version = os.getenv("VERSION", default="5.131")
    group_id = os.environ["GROUP_ID"]
    group_owner_id = os.environ["GROUP_OWNER_ID"]
    folder = "media"

    picture_url, transcript = get_comics()
    Path(folder).mkdir(parents=True, exist_ok=True)
    try:
        image_path = download_image(picture_url, folder)
        server_address = get_image_server_address(access_token, version, group_id)
        server, photo, hash_image = load_image(server_address, image_path)
        owner_id, media_id, text = save_image(server, photo, hash_image, transcript, access_token, version, group_id)
        publish_image(owner_id, media_id, text, access_token, version, group_owner_id)
    except requests.exceptions.HTTPError as error:
        print(f"Exception occurred. {error} \n")
    finally:
        os.remove(image_path)


if __name__ == "__main__":
    main()
