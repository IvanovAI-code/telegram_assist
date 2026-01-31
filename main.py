import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.settings import TELEGRAM_TOKEN
from bot.handlers import base, voice

# Настраиваем логирование (вывод информации)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция - запуск бота"""
    
    # Создаём объект бота
    bot = Bot(token=TELEGRAM_TOKEN)
    
    # Диспетчер = управляет обработчиками
    dp = Dispatcher()
    
    # Подключаем роутеры с обработчиками
    dp.include_router(base.router)
    dp.include_router(voice.router)

    logger.info("🤖 Бот запущен!")
    
    try:
        # Запускаем polling (бот постоянно спрашивает Telegram о новых сообщениях)
        await dp.start_polling(bot)
    finally:
        # При остановке - закрываем соединение
        await bot.session.close()


if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())
