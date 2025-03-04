import os
import time
import random
import logging
import argparse
import sys
import telegram
from PIL import Image
from image_downloader import download_all_images

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def publish_images(directory, delay_seconds, bot, channel_id):
    """
    Публикует изображения в Telegram-канал с указанной задержкой.

    Аргументы:
        directory (str): Папка с изображениями.
        delay_seconds (int): Задержка между публикациями в секундах.
        bot (telegram.Bot): Объект бота Telegram.
        channel_id (str): ID Telegram-канала.
    """
    error_count = 0
    max_errors = 5

    while True:
        images = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if len(images) == 0:
            logging.error("Ошибка: В папке нет изображений. Завершаем работу.")
            raise FileNotFoundError("В папке отсутствуют изображения для публикации. Добавьте фотографии и запустите программу снова.")

        random.shuffle(images)

        for image in images:
            try:
                with open(image, "rb") as photo:
                    bot.send_photo(chat_id=channel_id, photo=photo)
                    logging.info(f"Опубликовано: {image}")
                    error_count = 0

                time.sleep(delay_seconds)
            except (telegram.error.TelegramError, OSError, IOError) as e:
                error_count += 1
                logging.error(f"Ошибка при публикации {image}: {e}")

                if error_count >= max_errors:
                    logging.critical("Достигнуто максимальное количество ошибок. Завершаем работу.")
                    sys.exit(1)

def main():
    """
    Основная функция для запуска публикации изображений.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    publish_delay = int(os.getenv("PUBLISH_DELAY_HOURS", 4)) * 3600

    if not bot_token or not channel_id:
        logging.error("Не найдены TELEGRAM_BOT_TOKEN или TELEGRAM_CHANNEL_ID")
        return

    bot = telegram.Bot(token=bot_token)

    parser = argparse.ArgumentParser(description="Публикация изображений в Telegram-канал.")
    parser.add_argument("--directory", type=str, default=os.getenv("IMAGES_DIR", "images"), help="Папка с изображениями")
    parser.add_argument("--delay", type=int, default=publish_delay, help="Задержка между публикациями в секундах")
    args = parser.parse_args()

    publish_images(args.directory, args.delay, bot, channel_id)

if __name__ == "__main__":
    main()
