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

def load_and_shuffle_images(directory):
    """
    Загружает изображения из указанной папки и перемешивает их.

    Аргументы:
        directory (str): Путь к папке с изображениями.

    Возвращает:
        list: Перемешанный список путей к изображениям.
    """
    images = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not images:
        logging.error("Ошибка: В папке нет изображений. Завершаем работу.")
        raise FileNotFoundError("В папке отсутствуют изображения для публикации. Добавьте фотографии и запустите программу снова.")

    random.shuffle(images)
    return images

def publish_images(directory, delay_seconds, bot, channel_id):
    """
    Циклично публикует изображения в Telegram-канал с задержкой.

    Аргументы:
        directory (str): Папка с изображениями.
        delay_seconds (int): Задержка между публикациями в секундах.
        bot (telegram.Bot): Объект бота Telegram.
        channel_id (str): ID Telegram-канала.
    """
    failure_count = 0
    while True:
        images = load_and_shuffle_images(directory)

        for image in images:
            try:
                with open(image, "rb") as photo:
                    bot.send_photo(chat_id=channel_id, photo=photo)
                    logging.info(f"Опубликовано: {image}")
                time.sleep(delay_seconds)
                failure_count = 0
            except (telegram.error.TelegramError, OSError, IOError) as e:
                logging.error(f"Ошибка при публикации {image}: {e}")
                failure_count += 1
                sleep_time = min(2 ** failure_count, 3600)
                logging.info(f"Пауза на {sleep_time} секунд из-за ошибки подключения.")
                time.sleep(sleep_time)

        logging.info("Все изображения опубликованы. Начинаем заново.") 

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