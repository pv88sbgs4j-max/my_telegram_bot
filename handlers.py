from telebot import TeleBot
from datetime import datetime
import requests
from config import LEAGUE_NAME_TICKER, LEAGUE_IDS, url, headers
from keyboards import main_keyboard, action_keyboard, matches_keyboard
from api_client import get_match_details
from utils import get_today_date, format_match_details, is_match_date_passed
from cache import get_cached_matches, save_matches_to_cache
from api_client import get_matches_by_date
from cache import get_cached_lineups, save_lineups_to_cache, get_score_by_match_id, get_match_date_and_status, update_match_status_in_cache

user_state = {}

def register_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.chat.id, "⚽ Выбери лигу:", reply_markup=main_keyboard())

    @bot.message_handler(func=lambda message: message.text in LEAGUE_NAME_TICKER)
    def handle_league_choice(message):
        league_name = message.text
        user_state[message.chat.id] = {"league": league_name}
        bot.send_message(
            message.chat.id,
            f"Вы выбрали **{league_name}**. Выберите вариант:",
            reply_markup=action_keyboard(),
            parse_mode="Markdown"
        )

    @bot.message_handler(func=lambda message: message.text == "🔙 Назад")
    def handle_back_button(message):
        chat_id = message.chat.id
        if chat_id in user_state:
            del user_state[chat_id]
        bot.send_message(chat_id, "⚽ Выбери лигу:", reply_markup=main_keyboard())

    @bot.message_handler(func=lambda message: message.text == "📅 Сегодня")
    def handle_today_button(message):
        chat_id = message.chat.id
        if chat_id not in user_state:
            bot.reply_to(message, "❌ Сначала выберите лигу через /start")
            return
        league_name = user_state[chat_id].get("league")
        if not league_name:
            bot.reply_to(message, "❌ Ошибка: лига не выбрана.")
            return
        today_display = datetime.now().strftime("%d.%m.%Y")
        today_api = datetime.now().strftime("%Y%m%d")
        if show_matches(chat_id, league_name, today_api, today_display):
            del user_state[chat_id]

    @bot.message_handler(func=lambda message: message.text == "✏️ Ввести дату")
    def handle_manual_date_button(message):
        chat_id = message.chat.id
        if chat_id not in user_state:
            bot.reply_to(message, "❌ Сначала выберите лигу через /start")
            return
        bot.send_message(
            chat_id,
            "📅 Введите дату в формате **ДД.ММ.ГГГГ**\nНапример: 22.08.2026",
            parse_mode="Markdown"
        )

    @bot.message_handler(func=lambda message: True)
    def handle_date_input(message):
        chat_id = message.chat.id
        if chat_id not in user_state:
            return
        league_name = user_state[chat_id].get("league")
        if not league_name:
            return
        date_str = message.text.strip()
        try:
            input_date = datetime.strptime(date_str, "%d.%m.%Y")
            api_date = input_date.strftime("%Y%m%d")
            display_date = input_date.strftime("%d.%m.%Y")
        except ValueError:
            bot.reply_to(message, "❌ Неверный формат! Введите дату как **ДД.ММ.ГГГГ**", parse_mode="Markdown")
            return
        if show_matches(chat_id, league_name, api_date, display_date):
            del user_state[chat_id]

    @bot.callback_query_handler(func=lambda call: call.data.startswith("match_"))
    def handle_match_callback(call):
        match_id = int(call.data.split("_")[1])
        bot.answer_callback_query(call.id)
        try:
            match_info_cache = get_match_date_and_status(match_id)
            if match_info_cache:
                date_passed = is_match_date_passed(match_info_cache["date"])
                status = match_info_cache["status"]
                if date_passed and status != "FT":
                    cached = None
                    cached_score = None
                else:
                    cached = get_cached_lineups(match_id)
                    cached_score = get_score_by_match_id(match_id)
            else:
                cached = None
                cached_score = None
            cached = get_cached_lineups(match_id)
            cached_score = get_score_by_match_id(match_id)
            if cached is not None and cached_score is not None:
                home_data = cached["home"]
                away_data = cached["away"]
                score = cached_score["score"]
                time = cached_score["time"]
                match_info = {"score": score, "time": time}
            else:
                home_data, away_data, score_data = get_match_details(match_id)
                print(f"score data: {score_data}")
                score = score_data.get("response", {}).get("status", {}).get("scoreStr", "")
                print(f"score: {score}")
                time = score_data.get("response", {}).get("time", "")
                print(f"time: {time}")
                new_status = score_data.get("response", {}).get("status", {}).get("reason", {}).get("short", "")
                update_match_status_in_cache(match_id, new_status)
                save_lineups_to_cache(match_id, {"home": home_data, "away": away_data})
                match_info = {"score": score, "time": time}
            text = format_match_details(home_data, away_data, match_info)
            bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Ошибка: {e}")

    def show_matches(chat_id, league_name, api_date, display_date):
        league_id = LEAGUE_IDS.get(league_name)
        if not league_id:
            bot.send_message(chat_id, "❌ Ошибка: ID лиги не найден.")
            return False

        today_api = datetime.now().strftime("%Y%m%d")

        if api_date < today_api:
            cached = get_cached_matches(league_id, api_date)
            if cached is not None:
                filtered_matches = cached
            else:
                data = get_matches_by_date(api_date)
                filtered_matches = []
                for match in data.get("response", {}).get("matches", []):
                    if match.get("leagueId") == league_id:
                        filtered_matches.append(match)
                save_matches_to_cache(league_id, api_date, filtered_matches)
        else:
            data = get_matches_by_date(api_date)
            filtered_matches = []
            for match in data.get("response", {}).get("matches", []):
                if match.get("leagueId") == league_id:
                    filtered_matches.append(match)
            save_matches_to_cache(league_id, api_date, filtered_matches)

        if not filtered_matches:
            bot.send_message(chat_id, f"❌ Матчей для {league_name} на {display_date} не найдено.")
            return False
        bot.send_message(
            chat_id,
            f"⚽ **{league_name} — матчи на {display_date}**\n\nНажмите на матч для подробностей:",
            reply_markup=matches_keyboard(filtered_matches),
            parse_mode="Markdown"
        )
        return True