from telebot import TeleBot
from config import TOKEN
from handlers import register_handlers

bot = TeleBot(TOKEN)
register_handlers(bot)

print("🤖 Бот запущен...")
bot.infinity_polling()