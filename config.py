import os

def get_config():
    config = {
        "NASA_API_KEY": os.getenv("NASA_API_KEY"),
        "IMAGES_DIR": os.getenv("IMAGES_DIR", "images"),
        "APOD_URL": os.getenv("APOD_URL", "https://api.nasa.gov/planetary/apod"),
        "EPIC_URL": os.getenv("EPIC_URL", "https://api.nasa.gov/EPIC/api/natural/images"),
        "SPACEX_URL": os.getenv("SPACEX_URL", "https://api.spacexdata.com/v5/launches/past"),
        "PUBLISH_DELAY_HOURS": int(os.getenv("PUBLISH_DELAY_HOURS", 4)),
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_CHANNEL_ID": os.getenv("TELEGRAM_CHANNEL_ID")
    }
    if config["NASA_API_KEY"] is None:
        raise ValueError("NASA_API_KEY не задана")
    return config
