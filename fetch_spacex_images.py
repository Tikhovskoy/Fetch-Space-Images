import os
import argparse
from image_downloader import download_all_images

def main():
    """
    Основная функция для загрузки изображений SpaceX.
    Запрашивает изображения последнего запуска и сохраняет их в указанную папку.
    """
    parser = argparse.ArgumentParser(description="Скачивание изображений SpaceX.")
    parser.add_argument("--directory", type=str, default=os.getenv("IMAGES_DIR", "images"), help="Папка для сохранения изображений")
    args = parser.parse_args()

    download_all_images(directory=args.directory)

if __name__ == "__main__":
    main()
