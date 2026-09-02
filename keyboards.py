from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import LEAGUE_NAME_TICKER


def main_keyboard():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    
    for league_name in LEAGUE_NAME_TICKER.keys():
        item_button = KeyboardButton(league_name)
        markup.add(item_button)
    return markup

def action_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_today = KeyboardButton("📅 Сегодня")
    btn_manual = KeyboardButton("✏️ Ввести дату")
    btn_back = KeyboardButton("🔙 Назад")
    markup.add(btn_today, btn_manual, btn_back)
    return markup

def matches_keyboard(filtered_matches):
    markup = InlineKeyboardMarkup(row_width=1)  
    for match in filtered_matches:
        home = match.get("home", {}).get("name", "?")
        away = match.get("away", {}).get("name", "?")
        time = match.get("time", "—")
        button_text = f"{home} 🆚 {away}  {time}"
        match_id = match.get("id")
        button = InlineKeyboardButton(button_text, callback_data=f"match_{match_id}")
        markup.add(button)
    return markup

def ai_keyboard_for_not_stated(match_id):
    markup = InlineKeyboardMarkup(row_width=1)
    button_text_prediction = f"Получить прогноз на матч"
    button_prediction = InlineKeyboardButton(button_text_prediction, callback_data=f"prediction_{match_id}")
    markup.add(button_prediction)
    return markup

def ai_keyboard_for_ended(match_id):
    markup = InlineKeyboardMarkup(row_width=1)
    button_text_review = f"Получить краткий обзор на матч"
    button_review = InlineKeyboardButton(button_text_review, callback_data=f"review_{match_id}")
    markup.add(button_review)
    return markup