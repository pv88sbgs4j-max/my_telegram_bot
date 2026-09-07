from flask import Flask, request
import requests
from telebot import TeleBot, types
from config import TOKEN
from handlers import register_handlers
from database import init_db

app = Flask(__name__)
bot = TeleBot(TOKEN)
init_db()
register_handlers(bot)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

print("🤖 Бот запущен...")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://mytelegrambot-production-0b86.up.railway.app/webhook')
    app.run(host='0.0.0.0', port=443)