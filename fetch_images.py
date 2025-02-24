import requests
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
EPIC_API_URL = "https://api.nasa.gov/EPIC/api/natural/images"
EPIC_IMAGE_URL = "https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
SPACEX_URL = "https://api.spacexdata.com/v5/launches/past"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_nasa_apod_images(count=10):
    try:
        response = requests.get(NASA_APOD_URL, params={"api_key": NASA_API_KEY, "count": count}, timeout=10)
        response.raise_for_status()
        data = response.json()
        images = [item["url"] for item in data if item.get("media_type") == "image"]
        if not images:
            logging.warning("NASA APOD не вернуло изображений.")
        return images
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе NASA APOD: {e}")
        return []

def fetch_epic_images(count=10):
    try:
        response = requests.get(f"{EPIC_API_URL}?api_key={NASA_API_KEY}", timeout=10)
        response.raise_for_status()
        images_data = response.json()[:count]
        if not images_data:
            logging.warning("NASA EPIC не вернуло изображений.")
        return [
            EPIC_IMAGE_URL.format(
                year=datetime.strptime(img["date"], "%Y-%m-%d %H:%M:%S").strftime("%Y"),
                month=datetime.strptime(img["date"], "%Y-%m-%d %H:%M:%S").strftime("%m"),
                day=datetime.strptime(img["date"], "%Y-%m-%d %H:%M:%S").strftime("%d"),
                image_name=img["image"]
            ) + f"?api_key={NASA_API_KEY}"
            for img in images_data
        ]
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе NASA EPIC: {e}")
        return []

def fetch_spacex_images():
    try:
        response = requests.get(SPACEX_URL, timeout=10)
        response.raise_for_status()
        launches = response.json()
        images = next(
            (launch.get("links", {}).get("flickr", {}).get("original", []) for launch in reversed(launches) if launch.get("links", {}).get("flickr", {}).get("original")),
            []
        )
        if not images:
            logging.warning("SpaceX не вернуло изображений.")
        return images
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе SpaceX: {e}")
        return []
