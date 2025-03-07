import argparse
from image_downloader import download_all_images
from config import get_config

def main():
    """
    Основная функция для загрузки изображений NASA APOD.

    Аргументы командной строки:
        --count (int): Количество изображений для загрузки (по умолчанию 10).

    Функция вызывает `download_all_images()`, передавая папку сохранения и количество изображений.
    """
    config = get_config()

    parser = argparse.ArgumentParser(description="Скачивание изображений NASA APOD.")
    parser.add_argument("--directory", type=str, default=config["IMAGES_DIR"], help="Папка для сохранения изображений")
    parser.add_argument("--count", type=int, default=10, help="Количество изображений")
    args = parser.parse_args()

    download_all_images(
        directory=args.directory,
        count=args.count,
        api_key=config["NASA_API_KEY"],
        source="nasa_apod"
    )

if __name__ == "__main__":
    main()