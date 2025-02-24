import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
EPIC_API_URL = "https://api.nasa.gov/EPIC/api/natural/images"
EPIC_IMAGE_URL = "https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
SPACEX_URL = "https://api.spacexdata.com/v5/launches/past"

def fetch_nasa_apod_images(count=10):
    """Запрашивает изображения NASA APOD."""
    response = requests.get(NASA_APOD_URL, params={"api_key": NASA_API_KEY, "count": count}, timeout=10)
    response.raise_for_status()
    return [item["url"] for item in response.json() if item.get("media_type") == "image"]

def fetch_epic_images(count=10):
    """Запрашивает изображения EPIC."""
    response = requests.get(f"{EPIC_API_URL}?api_key={NASA_API_KEY}", timeout=10)
    response.raise_for_status()
    images = response.json()[:count]

    return [
        EPIC_IMAGE_URL.format(
            year=datetime.strptime(img["date"], "%Y-%m-%d %H:%M:%S").strftime("%Y"),
            month=datetime.strptime(img["date"], "%Y-%m-%d %H:%M:%S").strftime("%m"),
            day=datetime.strptime(img["date"], "%Y-%m-%d %H:%M:%S").strftime("%d"),
            image_name=img["image"]
        ) + f"?api_key={NASA_API_KEY}"
        for img in images
    ]

def fetch_spacex_images():
    """Находит последний запуск SpaceX с фотографиями и загружает изображения."""
    response = requests.get(SPACEX_URL, timeout=10)
    response.raise_for_status()
    
    launches = response.json()
    
    return next(
        (launch.get("links", {}).get("flickr", {}).get("original", []) for launch in reversed(launches) if launch.get("links", {}).get("flickr", {}).get("original")),
        []
    )