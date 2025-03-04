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

### **Как настроить переменные окружения**

**Способ 1: через файл **`` (рекомендуется)\
Создайте файл `.env` в корне проекта и добавьте туда:

```
TELEGRAM_BOT_TOKEN="your-bot-token"
TELEGRAM_CHANNEL_ID="your_channel_id"
PUBLISH_DELAY_HOURS=4
IMAGES_DIR="images"
```

**Способ 2: через экспорт в терминале**

```sh
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHANNEL_ID="your_channel_id"
export PUBLISH_DELAY_HOURS=4
export IMAGES_DIR="images"

## Установка и запуск

### 1. Установка зависимостей
Создайте виртуальное окружение и установите зависимости:
```sh
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate  # Для Windows
pip install -r requirements.txt
```

### 2. Создание `.env` файла
Создайте файл `.env` в корневой директории и добавьте в него:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id
PUBLISH_DELAY_HOURS=4
```
Эта переменная `PUBLISH_DELAY_HOURS` задает задержку между публикациями в часах (по умолчанию 4 часа).

### 3. Запуск скриптов

#### 3.1. Скачивание изображений вручную
```sh
python main.py --source all --count 5
```
Параметры:
- `--source`: источник изображений (`nasa_apod`, `epic`, `spacex`, `all`).
- `--count`: количество изображений для загрузки (по умолчанию 10).

#### 3.2. Автоматическая публикация в Telegram
```sh
python telegram_publisher.py --directory images --delay 14400
```
(14400 секунд = 4 часа, можно изменить в `.env` через `PUBLISH_DELAY_HOURS`).

#### 3.3. Запуск отдельных скриптов
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
