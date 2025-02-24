import argparse
from fetch_images import fetch_nasa_apod_images
from image_downloader import save_image, clear_directory

def main():
    parser = argparse.ArgumentParser(description="Скачивание изображений NASA APOD.")
    parser.add_argument("--count", type=int, default=10, help="Количество изображений")
    args = parser.parse_args()

    images = fetch_nasa_apod_images(args.count)
    directory = "images"
    clear_directory(directory)

    for index, url in enumerate(images, start=1):
        save_image(index, url, directory, "nasa")

if __name__ == "__main__":
    main()
