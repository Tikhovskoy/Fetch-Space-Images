# Fetch Space Images

## Описание
Этот проект предназначен для автоматического скачивания изображений из NASA APOD, NASA EPIC и SpaceX, а также их публикации в Telegram-канал с заданной периодичностью.

## Основные возможности
- **Автоматическое скачивание изображений** из источников:
  - NASA APOD
  - NASA EPIC
  - SpaceX
- **Публикация изображений в Telegram-канал** с заданной частотой (по умолчанию раз в 4 часа).
- **Настраиваемая задержка между публикациями** через переменную окружения `PUBLISH_DELAY_HOURS`.
- **Автоматическая подгрузка новых изображений**, если в папке осталось меньше 3 файлов.
- **Сжатие изображений**, если их размер превышает 20 MB.
- **Гибкие настройки через `.env` файл**.

## Настройка переменных окружения

Перед запуском программы необходимо задать следующие переменные окружения. Это позволит пользователю сразу понять, какие настройки требуются и как они влияют на работу программы.

## Переменные окружения

- **`NASA_API_KEY`**  
  **Описание:** API-ключ для доступа к данным NASA, используемый при запросах к NASA APOD и NASA EPIC.  
  **Пример значения:** `DEMO_KEY` или ваш персональный ключ.  
  **Влияние:** Без этого ключа запросы к API не будут работать.

- **`APOD_URL`**  
  **Описание:** URL для запроса изображений NASA APOD.  
  **Значение по умолчанию:** `https://api.nasa.gov/planetary/apod`  
  **Влияние:** Определяет конечную точку API для APOD.

- **`EPIC_URL`**  
  **Описание:** URL для запроса изображений NASA EPIC.  
  **Значение по умолчанию:** `https://api.nasa.gov/EPIC/api/natural/images`  
  **Влияние:** Определяет конечную точку API для EPIC.

- **`SPACEX_URL`**  
  **Описание:** URL для запроса изображений SpaceX.  
  **Значение по умолчанию:** `https://api.spacexdata.com/v5/launches/past`  
  **Влияние:** Используется для получения изображений последнего запуска SpaceX.

- **`TELEGRAM_BOT_TOKEN`**  
  **Описание:** Токен Telegram-бота для публикации изображений.  
  **Пример значения:** `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`  
  **Влияние:** Без корректного токена публикация в Telegram невозможна.

- **`TELEGRAM_CHANNEL_ID`**  
  **Описание:** Идентификатор Telegram-канала, куда будут отправляться изображения.  
  **Пример значения:** `@your_channel_name` или числовой ID  
  **Влияние:** Определяет канал для публикации фото.

- **`PUBLISH_DELAY_HOURS`**  
  **Описание:** Задержка между публикациями в Telegram (в часах).  
  **Значение по умолчанию:** `4`  
  **Влияние:** Определяет интервал между публикациями, что помогает избежать перегрузки.

- **`IMAGES_DIR`**  
  **Описание:** Папка, в которую будут сохраняться скачанные изображения.  
  **Значение по умолчанию:** `images`  
  **Влияние:** Указывает директорию для хранения изображений.

### **Как настроить переменные окружения**

**Способ 1: через файл** (рекомендуется)

Создайте файл `.env` в корне проекта и добавьте туда:

```dotenv
NASA_API_KEY=your_nasa_api_key
APOD_URL=https://api.nasa.gov/planetary/apod
EPIC_URL=https://api.nasa.gov/EPIC/api/natural/images
SPACEX_URL=https://api.spacexdata.com/v5/launches/past
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id
PUBLISH_DELAY_HOURS=4
IMAGES_DIR=image
```

**Способ 2: через экспорт в терминале**

```sh
export NASA_API_KEY="your_nasa_api_key"
export APOD_URL="https://api.nasa.gov/planetary/apod"
export EPIC_URL="https://api.nasa.gov/EPIC/api/natural/images"
export SPACEX_URL="https://api.spacexdata.com/v5/launches/past"
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export TELEGRAM_CHANNEL_ID="your_channel_id"
export PUBLISH_DELAY_HOURS=4
export IMAGES_DIR="images"
```

## Установка и запуск

### 1. Установка зависимостей
Создайте виртуальное окружение и установите зависимости:
```sh
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate  # Для Windows
pip install -r requirements.txt
```

### 2. Запуск скриптов

#### 2.1. Скачивание изображений вручную
```sh
python main.py --source all --count 5
```
Параметры:
- `--source`: источник изображений (`nasa_apod`, `epic`, `spacex`, `all`).
- `--count`: количество изображений для загрузки (по умолчанию 10).

#### 2.2. Автоматическая публикация в Telegram
```sh
python telegram_publisher.py --directory images --delay 14400
```
(14400 секунд = 4 часа, можно изменить в `.env` через `PUBLISH_DELAY_HOURS`).

#### 2.3. Запуск отдельных скриптов
- Скачивание изображений NASA APOD:
  ```sh
  python fetch_nasa_apod.py --count 5
  ```
- Скачивание изображений NASA EPIC:
  ```sh
  python fetch_nasa_epic.py --count 5
  ```
- Скачивание изображений SpaceX:
  ```sh
  python fetch_spacex_images.py
  ```

## Описание файлов
### `fetch_images.py`
- Запрашивает изображения из NASA APOD, NASA EPIC и SpaceX.
- Обрабатывает API-запросы и логирует ошибки.

### `image_downloader.py`
- Вспомогательный модуль для скачивания и сохранения изображений.
- Поддерживает автоматическое удаление старых файлов.
- Функция `download_all_images()` скачивает сразу все изображения.

### `fetch_nasa_apod.py`
- Загружает изображения NASA APOD.
- Вызывает `download_all_images()` и сохраняет файлы.

### `fetch_nasa_epic.py`
- Загружает изображения NASA EPIC.
- Вызывает `download_all_images()` и сохраняет файлы.

### `fetch_spacex_images.py`
- Загружает фотографии последнего запуска SpaceX.
- Вызывает `download_all_images()` и сохраняет файлы.

### `telegram_publisher.py`
- Публикует изображения в Telegram-канал.
- Поддерживает настройку задержки (`PUBLISH_DELAY_HOURS`).
- Если изображений мало, автоматически загружает новые.

### `main.py`
- Позволяет загружать изображения вручную через `--source`.
- Запускает нужные скрипты скачивания с параметрами.

## Лицензия
Проект распространяется под лицензией MIT. Полный текст лицензии доступен в файле `LICENSE`.

## Обратная связь
Если у вас есть вопросы или предложения, создайте issue в репозитории или отправьте pull request.
