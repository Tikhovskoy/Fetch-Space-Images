import os
import argparse
import subprocess

def run_script(script_name, args=[]):
    """Запускает скрипт с переданными аргументами."""
    subprocess.run(["python", script_name] + args)

def main():
    parser = argparse.ArgumentParser(description="Запуск скачивания изображений.")
    parser.add_argument("--source", choices=["nasa_apod", "epic", "spacex", "all"], default="all", help="Выбор источника")
    parser.add_argument("--count", type=str, default="10", help="Количество изображений")
    parser.add_argument("--launch_id", type=str, help="ID запуска SpaceX (если не указан, берется последний)")

    args = parser.parse_args()
    scripts = {
        "nasa_apod": ["fetch_nasa_apod.py", ["--count", args.count]],
        "epic": ["fetch_nasa_epic.py", ["--count", args.count]],
        "spacex": ["fetch_spacex_images.py", ["--launch_id", args.launch_id] if args.launch_id else []],
    }

    if args.source == "all":
        for script, script_args in scripts.values():
            run_script(script, script_args)
    else:
        run_script(*scripts[args.source])

if __name__ == "__main__":
    main()
