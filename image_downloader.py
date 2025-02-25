import os
import requests
import urllib.parse
import logging
from fetch_images import fetch_nasa_apod_images, fetch_epic_images, fetch_spacex_images

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_file_extension(url):
    return os.path.splitext(os.path.basename(urllib.parse.urlsplit(url).path))[1] or ".jpg"

def save_image(index, url, directory, prefix):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    image_path = os.path.join(directory, f"{prefix}{index}{get_file_extension(url)}")

    with open(image_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Сохранено: {image_path}")

def clear_directory(directory):
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    os.makedirs(directory, exist_ok=True)

def download_all_images(directory="images", count=5):
    os.makedirs(directory, exist_ok=True)

    sources = {
        "nasa_apod": fetch_nasa_apod_images(count),
        "epic": fetch_epic_images(count),
        "spacex": fetch_spacex_images()
    }

    for prefix, images in sources.items():
        if not images:
            logging.warning(f"Нет изображений для {prefix}. Пропускаем.")
            continue
        for index, url in enumerate(images, start=1):
            try:
                save_image(index, url, directory, prefix)
            except requests.RequestException as e:
                logging.error(f"Ошибка при скачивании {url}: {e}")
