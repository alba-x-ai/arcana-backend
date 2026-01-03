import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ================== НАСТРОЙКИ ==================

BOT_TOKEN = "8572579095:AAEGKsFxVEwQ-DyDVwkM8nyaiLoWk44Td28"

MINI_APP_URL = "https://alba-x-ai.github.io/arcana-miniapp/"

# ================== ИНИЦИАЛИЗАЦИЯ ==================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ================== /start ==================

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    text = (
        "Arcana is a quiet tarot space.\n\n"
        "Each day, one card.\n"
        "No repetition. No noise.\n\n"
        "Tap below to begin."
    )

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="🔮 Open Arcana",
            web_app=types.WebAppInfo(url=MINI_APP_URL)
        )
    )

    await message.answer(text, reply_markup=keyboard)

# ================== ЗАПУСК ==================

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
