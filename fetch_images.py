import requests
import logging
from datetime import datetime
from config import get_config
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_nasa_apod_images(api_key, count=10):
    """
    Получает список изображений из NASA APOD.

    Аргументы:
        api_key (str): API-ключ NASA.
        count (int): Количество изображений для загрузки.

    Возвращает:
        list: Список URL изображений.
    """
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "count": count}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    images = [item["url"] for item in data if item.get("media_type") == "image"]
    if not images:
        logging.warning("NASA APOD не вернуло изображений.")
    return images

def get_epic_images_data(api_key, count=10):
    """
    Получает данные изображений NASA EPIC из API.

    Аргументы:
        api_key (str): API-ключ NASA.
        count (int): Количество изображений для получения.

    Возвращает:
        list: Список словарей с данными изображений.
    """
    base_api_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}
    response = requests.get(base_api_url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()[:count]

def build_epic_image_url(image_data):
    """
    Строит URL для изображения NASA EPIC на основе переданных данных.

    Аргументы:
        image_data (dict): Словарь с данными изображения.
        base_url (str): Базовый URL для формирования итогового адреса.

    Возвращает:
        str: Сформированный URL изображения.
    """
    base_download_url = "https://epic.gsfc.nasa.gov/archive/natural"
    date_obj = datetime.strptime(image_data["date"], "%Y-%m-%d %H:%M:%S")
    year = date_obj.strftime("%Y")
    month = date_obj.strftime("%m")
    day = date_obj.strftime("%d")
    image_name = image_data["image"]
    return f"{base_download_url}/{year}/{month}/{day}/png/{image_name}.png"

def fetch_epic_images(api_key, count=10):
    """
    Получает список URL изображений NASA EPIC.

    Аргументы:
        api_key (str): API-ключ NASA.
        count (int): Количество изображений для загрузки.

    Возвращает:
        list: Список URL изображений.
    """
    images_data = get_epic_images_data(api_key, count)
    if not images_data:
        logging.warning("NASA EPIC не вернуло изображений.")
        return []
    return [build_epic_image_url(img) for img in images_data]

def fetch_spacex_images(count=10):
    """
    Получает список изображений последнего запуска SpaceX.

    Аргументы:
        count (int): Количество изображений для загрузки.

    Возвращает:
        list: Список URL изображений.
    """
    url = "https://api.spacexdata.com/v5/launches/past"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    launches = response.json()

    launch_images = []
    for launch in reversed(launches):
        links = launch.get("links", {})
        flickr = links.get("flickr", {})
        original_images = flickr.get("original", [])
        if original_images:
            launch_images = original_images
            break

    if not launch_images:
        logging.warning("SpaceX не вернуло изображений.")

    return launch_images

def main():
    """
    Основная функция для тестирования получения изображений.
    """
    config = get_config()
    api_key = config["NASA_API_KEY"]

    images_apod = fetch_nasa_apod_images(api_key, count=5)
    images_epic = fetch_epic_images(api_key, count=5)
    images_spacex = fetch_spacex_images(count=5)
    
    print("NASA APOD Images:", images_apod)
    print("NASA EPIC Images:", images_epic)
    print("SpaceX Images:", images_spacex)

if __name__ == "__main__":
    main()
