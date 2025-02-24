import os
import time
import random
import logging
import argparse
from dotenv import load_dotenv
import telegram
from PIL import Image
from image_downloader import download_all_images

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
PUBLISH_DELAY_HOURS = int(os.getenv("PUBLISH_DELAY_HOURS", 4)) * 3600
MIN_IMAGES_BEFORE_DOWNLOAD = int(os.getenv("MIN_IMAGES_BEFORE_DOWNLOAD", 3))

if not BOT_TOKEN or not CHANNEL_ID:
    logging.error("TELEGRAM_BOT_TOKEN или TELEGRAM_CHANNEL_ID не заданы в .env")
    exit(1)

bot = telegram.Bot(token=BOT_TOKEN)

def compress_image(image_path, max_size_mb=20):
    max_size_bytes = max_size_mb * 1024 * 1024
    if os.path.getsize(image_path) <= max_size_bytes:
        return image_path

    image = Image.open(image_path).convert("RGB")
    compressed_path = image_path.replace(".", "_compressed.")
    
    quality = 95
    while os.path.getsize(image_path) > max_size_bytes and quality > 10:
        image.save(compressed_path, "JPEG", quality=quality)
        quality -= 5

    return compressed_path if os.path.exists(compressed_path) else image_path

def publish_images(directory, delay_seconds):
    while True:
        images = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if len(images) < MIN_IMAGES_BEFORE_DOWNLOAD:
            logging.info(f"Осталось {len(images)} фото, загружаем новые...")
            download_all_images(directory, 5)
            images = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        random.shuffle(images)

        for image in images:
            try:
                compressed_image = compress_image(image)
                with open(compressed_image, "rb") as photo:
                    bot.send_photo(chat_id=CHANNEL_ID, photo=photo)
                    logging.info(f"Опубликовано: {compressed_image}")
                
                time.sleep(delay_seconds)
            except Exception as e:
                logging.error(f"Ошибка при публикации {image}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Автоматическая публикация изображений в Telegram-канал.")
    parser.add_argument("--directory", type=str, default="images", help="Папка с изображениями")
    parser.add_argument("--delay", type=int, default=PUBLISH_DELAY_HOURS, help="Задержка между публикациями в секундах")
    args = parser.parse_args()

    publish_images(args.directory, args.delay)

if __name__ == "__main__":
    main()
