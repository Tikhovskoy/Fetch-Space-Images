import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    config = {
        "NASA_API_KEY": os.getenv("NASA_API_KEY"),
        "IMAGES_DIR": os.getenv("IMAGES_DIR", "images"),
        "PUBLISH_DELAY_HOURS": int(os.getenv("PUBLISH_DELAY_HOURS", 4)),
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_CHANNEL_ID": os.getenv("TELEGRAM_CHANNEL_ID")
    }
    if config["NASA_API_KEY"] is None:
        raise ValueError("NASA_API_KEY не задана")
    return config
