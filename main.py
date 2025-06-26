import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from deep_translator import GoogleTranslator

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token="8050530823:AAFKuT-0BbVsPw9mR1JoTVxv-zSYhr46FGY")
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"你好, {message.from_user.first_name}!\n\n"
        "Я профессиональный бот-переводчик с русского на китайский.\n"
        "Просто отправьте мне текст на русском, и я переведу его максимально точно."
    )


# Обработчик команды /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📝 Просто отправьте текст на русском языке для перевода на китайский.\n\n"
        "🛠 Команды:\n"
        "/start - Начать работу\n"
        "/help - Эта справка"
    )


# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: types.Message):
    text = message.text

    # Игнорируем команды
    if text.startswith('/'):
        return

    try:
        # Выполняем перевод
        translator = GoogleTranslator(source='ru', target='zh-CN')
        translation = translator.translate(text)

        # Отправляем чистый перевод
        await message.answer(translation)

    except Exception as e:
        logger.error(f"Ошибка перевода: {e}")
        await message.answer('⚠️ Произошла ошибка при переводе. Попробуйте еще раз.')


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())