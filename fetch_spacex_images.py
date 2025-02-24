import argparse
from fetch_images import fetch_spacex_images
from image_downloader import save_image, clear_directory

def main():
    """Главная функция для скачивания изображений SpaceX."""
    parser = argparse.ArgumentParser(description="Скачивание изображений SpaceX.")
    args = parser.parse_args()

    images = fetch_spacex_images()
    if not images:
        print("Нет доступных изображений для последнего запуска SpaceX.")
        return

    directory = "images"
    clear_directory(directory)

    for index, url in enumerate(images, start=1):
        save_image(index, url, directory, "spacex")

if __name__ == "__main__":
    main()
