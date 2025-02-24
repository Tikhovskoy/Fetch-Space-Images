import os
import requests
import shutil
import urllib.parse
import logging
import argparse
from dotenv import load_dotenv
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_extension(url):
    """Получает расширение файла из URL."""
    return os.path.splitext(os.path.basename(urllib.parse.urlsplit(url).path))[1] or ".jpg"

def clear_directory(directory):
    """Очищает указанную директорию перед скачиванием."""
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory, exist_ok=True)

def download_images(fetch_function, api_type, directory, prefix, count=10):
    """Скачивает изображения и сохраняет их в указанную папку."""
    image_links = fetch_function(api_type, count)
    if not image_links:
        logging.warning(f"Нет изображений для {directory}")
        return
    
    for index, url in enumerate(image_links, start=1):
        try:
            save_image(index, url, directory, prefix)
        except requests.RequestException as e:
            logging.error(f"Ошибка при скачивании изображения {url}: {e}")

def save_image(index, url, directory, prefix):
    """Скачивает и сохраняет одно изображение."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    image_path = os.path.join(directory, f"{prefix}{index}{get_file_extension(url)}")
    with open(image_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Сохранено: {image_path}")

def fetch_images(api_type, nasa_api_key, count=10):
    """Запрашивает изображения из указанного API."""
    nasa_apod_url = "https://api.nasa.gov/planetary/apod"
    epic_api_url = "https://api.nasa.gov/EPIC/api/natural/images"
    epic_image_url = "https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
    spacex_url = "https://api.spacexdata.com/v5/launches/past"
    
    api_urls = {
        "nasa_apod": nasa_apod_url,
        "epic": f"{epic_api_url}?api_key={nasa_api_key}",
        "spacex": spacex_url
    }
    
    if api_type not in api_urls:
        raise ValueError(f"Неизвестный API: {api_type}")
    
    try:
        response = requests.get(api_urls[api_type], params={"api_key": nasa_api_key, "count": count} if api_type == "nasa_apod" else {}, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logging.error(f"Ошибка при получении данных из {api_type}: {e}")
        return []
    
    parsers = {
        "nasa_apod": lambda d: [item["url"] for item in d if item.get("media_type") == "image"],
        "epic": lambda d: [epic_image_url.format(year=img["date"][:4], month=img["date"][5:7], day=img["date"][8:10], image_name=img["image"]) + f"?api_key={nasa_api_key}" for img in d[:count]],
        "spacex": lambda d: next((launch["links"]["flickr"]["original"] for launch in reversed(d) if launch["links"].get("flickr", {}).get("original")), [])
    }
    
    return parsers[api_type](data)

def main():
    """Основная логика выполнения скрипта."""
    load_dotenv()
    nasa_api_key = os.getenv("NASA_API_KEY")
    if not nasa_api_key:
        raise ValueError("Ошибка: отсутствует NASA_API_KEY. Укажите его в .env")
    
    parser = argparse.ArgumentParser(description="Скачивание изображений из NASA, EPIC и SpaceX API.")
    parser.add_argument("--source", choices=["nasa_apod", "epic", "spacex", "all"], default="all", help="Выбор источника изображений")
    parser.add_argument("--count", type=int, default=10, help="Количество изображений для загрузки")
    args = parser.parse_args()
    
    image_directory = "images"
    os.makedirs(image_directory, exist_ok=True)
    
    sources = {
        "nasa_apod": [("nasa_apod", image_directory, "nasa", args.count)],
        "epic": [("epic", image_directory, "epic", args.count)],
        "spacex": [("spacex", image_directory, "spacex", args.count)],
        "all": [
            ("nasa_apod", image_directory, "nasa", args.count),
            ("epic", image_directory, "epic", args.count),
            ("spacex", image_directory, "spacex", args.count)
        ]
    }
    
    for api_type, directory, prefix, count in sources[args.source]:
        try:
            download_images(lambda at, c: fetch_images(at, nasa_api_key, c), api_type, directory, prefix, count)
        except Exception as e:
            logging.error(f"Ошибка при обработке {api_type}: {e}")

if __name__ == "__main__":
    main()
