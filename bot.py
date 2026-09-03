from telebot import TeleBot
from config import TOKEN
from handlers import register_handlers
from database import init_db

bot = TeleBot(TOKEN)
init_db()
register_handlers(bot)

print("🤖 Бот запущен...")
bot.infinity_polling()