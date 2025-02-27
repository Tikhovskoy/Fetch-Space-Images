import argparse
from image_downloader import download_all_images

def main():
    """
    Основная функция для загрузки изображений SpaceX.
    Запрашивает изображения последнего запуска и сохраняет их в указанную папку.
    """
    download_all_images(directory="images")

if __name__ == "__main__":
    main()
