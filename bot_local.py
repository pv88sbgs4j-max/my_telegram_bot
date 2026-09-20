from telebot import TeleBot
from config import TOKEN
from handlers import register_handlers
from database import init_db
from logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)   

init_db()

bot = TeleBot(TOKEN)

register_handlers(bot)

logger.info("🤖 Бот запущен локально в режиме polling...")


bot.remove_webhook()
bot.infinity_polling()