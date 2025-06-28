import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from deep_translator import GoogleTranslator

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение токена из переменных окружения
BOT_TOKEN = os.getenv("8050530823:AAFKuT-0BbVsPw9mR1JoTVxv-zSYhr46FGY")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable is not set!")
    exit(1)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        await message.answer(
            f"你好, {message.from_user.first_name}!\n\n"
            "Я профессиональный бот-переводчик с русского на китайский.\n"
            "Просто отправьте мне текст на русском, и я переведу его максимально точно."
        )
    except Exception as e:
        logger.error(f"Error in /start: {e}")


# Обработчик команды /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    try:
        await message.answer(
            "📝 Просто отправьте текст на русском языке для перевода на китайский.\n\n"
            "🛠 Команды:\n"
            "/start - Начать работу\n"
            "/help - Эта справка"
        )
    except Exception as e:
        logger.error(f"Error in /help: {e}")


# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: types.Message):
    try:
        text = message.text

        # Игнорируем команды
        if text.startswith('/'):
            return

        # Выполняем перевод
        translator = GoogleTranslator(source='ru', target='zh-CN')
        translation = translator.translate(text)

        # Отправляем чистый перевод
        await message.answer(translation)

    except Exception as e:
        logger.error(f"Translation error: {e}")
        try:
            await message.answer('⚠️ Произошла ошибка при переводе. Попробуйте еще раз.')
        except:
            logger.error("Failed to send error message")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())