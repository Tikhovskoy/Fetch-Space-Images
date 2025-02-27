import os
import argparse
import subprocess
import sys
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_script(script_name, args=[]):
    """
    Запускает внешний скрипт с указанными аргументами.

    Аргументы:
        script_name (str): Имя исполняемого скрипта.
        args (list): Список аргументов командной строки.

    Исключения:
        subprocess.CalledProcessError: Ошибка при выполнении внешнего скрипта.
    """
    try:
        logging.info(f"Запускаем: {script_name} {' '.join(args)}")
        subprocess.run([sys.executable, script_name] + args, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка выполнения {script_name}: {e}")

def main():
    """
    Основная функция, инициализирующая переменные окружения и запускающая загрузку изображений.

    Аргументы командной строки:
        --source (str): Источник изображений (nasa_apod, epic, spacex, all).
        --count (int): Количество загружаемых изображений.

    В зависимости от переданного параметра `--source`, запускает соответствующий скрипт.
    """
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Запуск скачивания изображений.")
    parser.add_argument("--source", choices=["nasa_apod", "epic", "spacex", "all"], default="all", help="Выбор источника")
    parser.add_argument("--count", type=str, default="10", help="Количество изображений")
    args = parser.parse_args()

    scripts = {
        "nasa_apod": ["fetch_nasa_apod.py", ["--count", args.count]],
        "epic": ["fetch_nasa_epic.py", ["--count", args.count]],
        "spacex": ["fetch_spacex_images.py", []]
    }

    if args.source == "all":
        for script, script_args in scripts.values():
            run_script(script, script_args)
    else:
        run_script(scripts[args.source][0], scripts[args.source][1])

if __name__ == "__main__":
    main()
