import argparse
from fetch_images import fetch_epic_images
from image_downloader import save_image, clear_directory

def main():
    parser = argparse.ArgumentParser(description="Скачивание изображений NASA EPIC.")
    parser.add_argument("--count", type=int, default=10, help="Количество изображений")
    args = parser.parse_args()

    images = fetch_epic_images(args.count)
    directory = "images"
    clear_directory(directory)

    for index, url in enumerate(images, start=1):
        save_image(index, url, directory, "epic")

if __name__ == "__main__":
    main()
