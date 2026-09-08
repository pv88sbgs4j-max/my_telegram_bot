# bot_local.py
from telebot import TeleBot
from config import TOKEN
from handlers import register_handlers
from database import init_db


init_db()

bot = TeleBot(TOKEN)

register_handlers(bot)

print("🤖 Бот запущен локально в режиме polling...")



bot.infinity_polling()