import logging
import os

from flask import Flask, request
from telebot import TeleBot, types

from config import TOKEN
from handlers import register_handlers
from database import init_db
from logger import setup_logging


setup_logging()
logger = logging.getLogger(__name__)   

app = Flask(__name__)
bot = TeleBot(TOKEN)
init_db()
register_handlers(bot)

logger.info("🤖 Бот запущен...")

@app.route('/webhook', methods=['POST'])
def webhook():
    update = types.Update.de_json(request.stream.read().decode('utf-8'))
    logger.debug(f"Получен update: {update.update_id}")
    bot.process_new_updates([update])
    return 'ok', 200


if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://mytelegrambot-production-beb5.up.railway.app/webhook')
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Запуск на порту {port}")
    app.run(host='0.0.0.0', port=port)