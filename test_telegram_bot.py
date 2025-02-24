import telegram
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = "-1002460010506" 

bot = telegram.Bot(token=BOT_TOKEN)

def send_photo(image_path):
    """Отправляет изображение в Telegram-канал."""
    with open(image_path, "rb") as photo:
        bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption="Фото из космоса")

if __name__ == "__main__":
    image_directory = "images"
    images = [f for f in os.listdir(image_directory) if f.endswith((".jpg", ".png", ".jpeg"))]

    if images:
        image_path = os.path.join(image_directory, images[0])
        send_photo(image_path)
        print(f"Отправлено: {image_path}")
    else:
        print("Нет изображений для отправки.")
