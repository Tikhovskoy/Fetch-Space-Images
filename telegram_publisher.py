import telegram
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = "-1002460010506"  # Правильный `chat_id`

bot = telegram.Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHANNEL_ID, text="Бот успешно отправил сообщение в канал!")
