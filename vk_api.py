import os
import os.path

import requests
from dotenv import load_dotenv

from downloader import download_image
from xkcd_comics import get_comics


def get_image_server_address(access_token, version, group_id):
    payload = {"group_id":group_id, "access_token":access_token, "v":version}
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    response = requests.get(url, payload)
    response.raise_for_status()
    server_address = response.json()["response"]["upload_url"]
    return server_address


def load_image(server_address, image_path):
    with open(image_path, 'rb') as file:
        url = server_address
        files = {'photo': file}
        response = requests.post(url, files=files)
        response.raise_for_status()
        server = response.json()["server"]
        photo = response.json()["photo"]
        image_hash = response.json()["hash"]
    return server, photo, image_hash


def save_image(server, photo, image_hash, transcript, access_token, version, group_id):
    payload = {
        "group_id":group_id,
        "photo":photo,
        "server":server,
        "hash":image_hash,
        "caption":transcript,
        "access_token":access_token,
        "v":version,
    }
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    response = requests.post(url, params=payload)
    response.raise_for_status()
    owner_id = response.json()['response'][0]["owner_id"]
    media_id = response.json()['response'][0]["id"]
    text = response.json()['response'][0]["text"]
    return owner_id, media_id, text


def publish_image(owner_id, media_id, text, access_token, version, group_owner_id):
    payload = {
        "owner_id": f"-{group_owner_id}",
        "from_group":1,
        "attachments": f"photo{owner_id}_{media_id}",
        "message": text,
        "access_token":access_token,
        "v":version,
    }
    url = "https://api.vk.com/method/wall.post"
    response = requests.post(url, params=payload)
    response.raise_for_status()
    return response.json()


def remove_file(picture_path):
    os.remove(picture_path)


def main():
    load_dotenv()
    access_token = os.getenv("VK_TOKEN")
    version = os.getenv("VERSION")
    group_id = os.getenv("GROUP_ID")
    group_owner_id = os.getenv("GROUP_OWNER_ID")

    picture_url, transcript = get_comics()
    image_path = download_image(picture_url)
    server_address = get_image_server_address(access_token, version, group_id)
    server, photo, hash_image = load_image(server_address, image_path)
    owner_id, media_id, text = save_image(server, photo, hash_image, transcript, access_token, version, group_id)
    publish_image(owner_id, media_id, text, access_token, version, group_owner_id)
    remove_file(image_path)


if __name__ == "__main__":
    main()
