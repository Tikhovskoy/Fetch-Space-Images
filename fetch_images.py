import requests
import logging
from datetime import datetime
from urllib.parse import urlencode
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_nasa_apod_images(api_key, url, count=10):
    """
    Получает список изображений из NASA APOD.

    Аргументы:
        api_key (str): API-ключ NASA.
        url (str): URL для запроса APOD.
        count (int): Количество изображений для загрузки.

    Возвращает:
        list: Список URL изображений.
    """
    params = {"api_key": api_key, "count": count}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    images = [item["url"] for item in data if item.get("media_type") == "image"]
    if not images:
        logging.warning("NASA APOD не вернуло изображений.")
    return images

def fetch_epic_images(api_key, url, count=10):
    """
    Получает список изображений NASA EPIC.

    Аргументы:
        api_key (str): API-ключ NASA.
        url (str): URL для запроса EPIC.
        count (int): Количество изображений для загрузки.

    Возвращает:
        list: Список URL изображений.
    """
    params = {"api_key": api_key}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    images_data = response.json()[:count]
    if not images_data:
        logging.warning("NASA EPIC не вернуло изображений.")

    epic_urls = []
    for img in images_data:
        date_obj = datetime.strptime(img["date"], "%Y-%m-%d %H:%M:%S")
        year = date_obj.strftime("%Y")
        month = date_obj.strftime("%m")
        day = date_obj.strftime("%d")
        image_name = img["image"]

        epic_url = f"{url}/{year}/{month}/{day}/png/{image_name}.png"
        epic_urls.append(epic_url)

    return epic_urls

def fetch_spacex_images(url, count=10):
    """
    Получает список изображений последнего запуска SpaceX.

    Аргументы:
        url (str): URL для запроса SpaceX.
        count (int): Количество изображений для загрузки.

    Возвращает:
        list: Список URL изображений.
    """
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
    api_key = os.getenv("NASA_API_KEY")
    apod_url = "https://api.nasa.gov/planetary/apod"
    epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    spacex_url = "https://api.spacexdata.com/v5/launches/past"

    if not api_key:
        logging.error("API-ключ NASA не найден в переменных окружения.")
        return

    images_apod = fetch_nasa_apod_images(api_key, apod_url, count=5)
    images_epic = fetch_epic_images(api_key, epic_url, count=5)
    images_spacex = fetch_spacex_images(spacex_url, count=5)
    
    print("NASA APOD Images:", images_apod)
    print("NASA EPIC Images:", images_epic)
    print("SpaceX Images:", images_spacex)

if __name__ == "__main__":
    main()
