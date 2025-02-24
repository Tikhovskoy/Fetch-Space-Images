import os
import argparse
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_script(script_name, args=[]):
    try:
        logging.info(f"Запускаем: {script_name} {' '.join(args)}")
        subprocess.run(["python", script_name] + args, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка выполнения {script_name}: {e}")

def main():
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
