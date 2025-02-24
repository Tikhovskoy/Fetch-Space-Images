import os
import requests
import urllib.parse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_extension(url):
    """Получает расширение файла из URL."""
    return os.path.splitext(os.path.basename(urllib.parse.urlsplit(url).path))[1] or ".jpg"

def save_image(index, url, directory, prefix):
    """Скачивает и сохраняет одно изображение."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    image_path = os.path.join(directory, f"{prefix}{index}{get_file_extension(url)}")
    with open(image_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Сохранено: {image_path}")

def clear_directory(directory):
    """Очищает указанную директорию перед скачиванием."""
    if os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
