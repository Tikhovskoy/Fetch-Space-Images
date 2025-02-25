import requests
import os
import logging
from datetime import datetime
from urllib.parse import urlencode

NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
EPIC_API_URL = "https://api.nasa.gov/EPIC/api/natural/images"
EPIC_IMAGE_URL = "https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
SPACEX_URL = "https://api.spacexdata.com/v5/launches/past"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_nasa_apod_images(count=10):
    params = {"api_key": NASA_API_KEY, "count": count}
    response = requests.get(NASA_APOD_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    images = [item["url"] for item in data if item.get("media_type") == "image"]
    if not images:
        logging.warning("NASA APOD не вернуло изображений.")
    return images

def fetch_epic_images(count=10):
    params = {"api_key": NASA_API_KEY}
    response = requests.get(EPIC_API_URL, params=params, timeout=10)
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

        epic_url = EPIC_IMAGE_URL.format(year=year, month=month, day=day, image_name=image_name)
        epic_url += "?" + urlencode(params)
        epic_urls.append(epic_url)

    return epic_urls

def fetch_spacex_images():
    response = requests.get(SPACEX_URL, timeout=10)
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
