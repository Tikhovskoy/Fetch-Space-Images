import argparse
from image_downloader import download_all_images

def main():
    parser = argparse.ArgumentParser(description="Скачивание изображений NASA EPIC.")
    parser.add_argument("--count", type=int, default=10, help="Количество изображений")
    args = parser.parse_args()

    download_all_images(directory="images", count=args.count)

if __name__ == "__main__":
    main()
