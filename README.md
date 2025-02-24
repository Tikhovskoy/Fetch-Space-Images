# Fetch Space Images

## Описание
Этот проект представляет собой скрипт для автоматического скачивания изображений из NASA APOD и EPIC API. Программа позволяет загружать астрофотографии дня (APOD) и снимки Земли, сделанные спутником DSCOVR, и сохранять их в одной папке.

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/fetch-space-images.git
cd fetch-space-images
```

### 2. Установка зависимостей
Рекомендуется использовать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate  # Для Windows
```

Затем установите необходимые зависимости:
```bash
pip install -r requirements.txt
```

### 3. Настройка API-ключа
Для работы с NASA API необходимо зарегистрировать API-ключ на [api.nasa.gov](https://api.nasa.gov/). После получения ключа создайте в корневой директории файл `.env` и добавьте в него:
```
NASA_API_KEY=your_api_key_here
```

## Использование

Запустите скрипт с необходимыми параметрами:
```bash
python main.py --source nasa_apod --count 5
```

### Доступные аргументы:
- `--source` — источник изображений (`nasa_apod`, `epic` или `all`). По умолчанию `all`.
- `--count` — количество изображений для загрузки (по умолчанию `10`).

### Примеры:
- Скачать 5 изображений APOD:
  ```bash
  python main.py --source nasa_apod --count 5
  ```
- Скачать 10 снимков Земли:
  ```bash
  python main.py --source epic --count 10
  ```
- Скачать изображения из всех доступных источников:
  ```bash
  python main.py --source all --count 20
  ```

## Описание функций

### `fetch_images(api_type, nasa_api_key, count=10)`
Запрашивает ссылки на изображения из NASA API.
- `api_type` – источник (`nasa_apod`, `epic`).
- `nasa_api_key` – API-ключ NASA.
- `count` – количество изображений.

### `download_images(fetch_function, api_type, directory, prefix, count=10)`
Скачивает изображения и сохраняет их в указанную директорию.
- `fetch_function` – функция для получения списка изображений.
- `api_type` – источник данных.
- `directory` – директория для сохранения.
- `prefix` – префикс имен файлов.
- `count` – количество изображений.

### `save_image(index, url, directory, prefix)`
Скачивает изображение по URL и сохраняет его.
- `index` – порядковый номер изображения.
- `url` – ссылка на изображение.
- `directory` – папка для сохранения.
- `prefix` – префикс имени файла.

### `clear_directory(directory)`
Удаляет содержимое указанной директории перед загрузкой новых изображений.
- `directory` – путь к папке.

### `get_file_extension(url)`
Определяет расширение файла из URL.
- `url` – ссылка на изображение.

## Структура проекта
```
fetch-space-images/
│── images/          # Папка для загруженных изображений
│── main.py          # Основной скрипт
│── requirements.txt # Файл с зависимостями
│── .env             # Конфигурационный файл с API-ключом (не загружать в репозиторий)
│── README.md        # Документация
```

## Лицензия
Проект распространяется под лицензией MIT. Полный текст лицензии доступен в файле `LICENSE`.

## Обратная связь
Если у вас есть вопросы или предложения, создайте issue в репозитории или отправьте pull request.
