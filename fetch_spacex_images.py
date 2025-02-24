import argparse
from image_downloader import download_all_images

def main():
    parser = argparse.ArgumentParser(description="Скачивание изображений SpaceX.")
    args = parser.parse_args()

    download_all_images(directory="images")

if __name__ == "__main__":
    main()
