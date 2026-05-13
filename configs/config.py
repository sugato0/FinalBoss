from environs import Env

# Загружаем настройки из файла .env.
# Там хранится токен бота, чтобы не писать его прямо в коде.
env=Env()
env.read_env()

# Достаем токен бота из настроек.
BOT_TOKEN= env("BOT_TOKEN")
