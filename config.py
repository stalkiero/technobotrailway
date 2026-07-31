import os

# Токен бота беремо зі змінної середовища BOT_TOKEN, або підставте свій напряму.
BOT_TOKEN = os.getenv("BOT_TOKEN", "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE")

# Директорія, де зберігаються окремі SQLite-бази для кожного користувача.
DB_DIR = os.getenv("DB_DIR", "data")

# Типи виходів: ключ -> (заголовок, тривалість у хвилинах або None, якщо без ліміту)
EXIT_TYPES = {
    "pererva": {"title": "☕ Перерва", "minutes": 10},
    "obid": {"title": "🍽 Обід", "minutes": 20},
    "tryvoga": {"title": "🚨 Тривога", "minutes": None},
    "peremishchennya": {"title": "🚶 Переміщення", "minutes": None},
}

# Скільки хвилин додає кнопка "Затримка"
DELAY_MINUTES = 5

# Як часто (сек) оновлювати повідомлення з таймером
TIMER_UPDATE_INTERVAL = 20
