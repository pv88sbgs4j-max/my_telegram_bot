import logging
from datetime import datetime, timedelta


import requests
from telebot import TeleBot

from ai_client import ask_deepseek
from api_client import get_match_details, get_matches_by_date
from config import LEAGUE_NAME_TICKER, LEAGUE_IDS, url, headers
from database import *
from keyboards import *
from utils import get_today_date, format_match_details, is_match_date_passed


logger = logging.getLogger(__name__)

user_state = {}

def register_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.chat.id, "⚽ Выбери лигу:", reply_markup=main_keyboard())

    @bot.message_handler(func=lambda message: message.text in LEAGUE_NAME_TICKER)
    def handle_league_choice(message):
        chat_id = message.chat.id
        league_name = message.text
        logger.info(f"{chat_id} выбрал лигу {league_name}")
        save_user_state(chat_id, league_name, None, None)
        bot.send_message(
            message.chat.id,
            f"Вы выбрали **{league_name}**. Выберите вариант:",
            reply_markup=action_keyboard(),
            parse_mode="Markdown"
        )

    @bot.message_handler(func=lambda message: message.text == "🔙 Назад")
    def handle_back_button(message):
        chat_id = message.chat.id
        logger.info(f"Пользователь {chat_id} нажал 'Назад'")
        if chat_id in user_state:
            del user_state[chat_id]
        bot.send_message(chat_id, "⚽ Выбери лигу:", reply_markup=main_keyboard())

    @bot.message_handler(func=lambda message: message.text == "📅 Сегодня")
    def handle_today_button(message):
        chat_id = message.chat.id
        state = get_user_state(chat_id)
        if not state:
            logger.debug(f"Сброс состояния для chat_id {chat_id}")
            bot.reply_to(message, "❌ Сначала выберите лигу через /start")
            return
        league_name = state.get("last_league")
        if not league_name:
            logger.debug(f"Ошибка: лига не выбрана.")
            bot.reply_to(message, "❌ Ошибка: лига не выбрана.")
            return
        today_display = datetime.now().strftime("%d.%m.%Y")
        today_api = datetime.now().strftime("%Y%m%d")
        logger.info(f"Пользователь {chat_id} выбрал сегодняшнюю дату")
        show_matches(chat_id, league_name, today_api, today_display)

    @bot.message_handler(func=lambda message: message.text == "✏️ Ввести дату")
    def handle_manual_date_button(message):
        chat_id = message.chat.id
        user_state = get_user_state(chat_id)
        if not user_state:
            bot.reply_to(message, "❌ Сначала выберите лигу через /start")
            logger.debug(f"Ошибка: лига не выбрана.")
            return
        bot.send_message(
            chat_id,
            "📅 Введите дату в формате **ДД.ММ.ГГГГ**\nНапример: 22.08.2026",
            parse_mode="Markdown"
        )


    @bot.message_handler(func=lambda message: message.text == "⬅️ К матчам")
    def handle_back_to_matches(message):
        chat_id = message.chat.id
        state = get_user_state(chat_id)
        if not state:
            bot.reply_to(message, "❌ Нет данных для возврата.")
            logger.debug(f"Ошибка: для пользователя {chat_id} нет данных для возврата.")
            return
        league_name = state.get("last_league")
        last_date = state.get("last_api_date")
        last_display_date = state.get("last_display_date")

        if not league_name or not last_date:
            logger.debug(f"Ошибка: для пользователя {chat_id} не удалось восстановить список матчей.")
            bot.reply_to(message, "❌ Не удалось восстановить список матчей.")
        else:
            show_matches(chat_id, league_name, last_date, last_display_date)
            logger.info(f"Пользователь {chat_id} вернулся обратно к матчам {last_display_date}")
            bot.send_message(message.chat.id,f"Вы выбрали **{league_name}**. Выберите вариант:",reply_markup=action_keyboard(),parse_mode="Markdown")


    @bot.message_handler(func=lambda message: True)
    def handle_date_input(message):
        chat_id = message.chat.id
        state = get_user_state(chat_id)
        if not state:
            return
        league_name = state.get("last_league")
        if not league_name:
            return
        date_str = message.text.strip()
        try:
            input_date = datetime.strptime(date_str, "%d.%m.%Y")
            api_date = input_date.strftime("%Y%m%d")
            display_date = input_date.strftime("%d.%m.%Y")
            logger.info(f"Пользователь {chat_id} выбрал {display_date} дату")
        except ValueError:
            bot.reply_to(message, "❌ Неверный формат! Введите дату как **ДД.ММ.ГГГГ**", parse_mode="Markdown")
            logger.debug(f"Ошибка: пользователь {chat_id} выбрал неверную дату.")
            return 
        show_matches(chat_id, league_name, api_date, display_date)
        


    @bot.callback_query_handler(func = lambda call: call.data.startswith("prediction_"))
    def handle_prediction(call):
        match_id = int(call.data.split("_")[1])
        bot.answer_callback_query(call.id)
        chat_id = call.message.chat.id
        cached = get_match_by_id(match_id)
        cached_prediction = get_prediction(match_id)
        if cached_prediction:
            prediction = cached_prediction["prediction"]
        else:  
            home = cached["home_team"]
            away = cached["away_team"]
            time = cached["time"]
            try:
                prompt = f"Спрогнозируй результат матча между {home} и {away} они играют {time}. Используй статистику, кто фаворит, кто аутсайдер. Необязательно давать прогноз на счет, можно давать прогнозы на угловые, удары а створ если о этом явно говорит статистика, но и на счет(фору) можешь давать прогноз. Ответ пиши на русском"
                bot.send_message(call.message.chat.id, "🧠 Думаю...")
                prediction = ask_deepseek(prompt)
                logger.info(f"Пользователь {chat_id} получил прогноз")
                save_prediction(match_id, prediction)
            except Exception as e:
                logger.debug(f"Ошибка: {e}")
                bot.send_message(call.message.chat.id, f"❌ Ошибка: {e}")
        bot.send_message(call.message.chat.id, prediction, parse_mode="HTML")


    @bot.callback_query_handler(func = lambda call: call.data.startswith("review_"))
    def handle_review(call):
        match_id = int(call.data.split("_")[1])
        bot.answer_callback_query(call.id)
        chat_id = call.message.chat.id
        cached = get_match_by_id(match_id)
        cahched_review = get_review(match_id)

        if cahched_review:
            review = cahched_review["review"]
        else:
            home = cached["home_team"]
            away = cached["away_team"]
            time = cached["time"]
            try:
                prompt = f"Дай краткий обзор матча между {home} и {away}. Они играли {time}. Расскажи на каких минутах происходили ключевые события"
                bot.send_message(call.message.chat.id, "🧠 Думаю...")
                review = ask_deepseek(prompt)
                logger.info(f"Пользователь {chat_id} получил обзор")
                save_review(match_id, review)
            except Exception as e:
                logger.debug(f"Ошибка: {e}")
                bot.send_message(call.message.chat.id, f"❌ Ошибка: {e}")
        bot.send_message(call.message.chat.id, review, parse_mode="HTML")


    def show_matches(chat_id:int, league_name:str, api_date:str, display_date:str) -> bool:
        try:
            league_id = LEAGUE_IDS.get(league_name)
            if not league_id:
                logger.debug(f"Ошибка: для {chat_id} не найден ID лиги")
                bot.send_message(chat_id, "❌ Ошибка: ID лиги не найден.")
                return False
            save_user_state(chat_id, league_name, api_date, display_date)
            filtered_matches =[]
            today_api = datetime.now().strftime("%Y%m%d")
            if api_date < today_api:
                cached = get_matches(league_id, api_date)
                logger.info(f"КЭШ: {len(cached)} матчей для лиги {league_name} на {api_date}")
                update = False
                for match in cached:
                    status = match.get("status", "")
                    if status != "FT":
                        update = True
                if cached and update == False:
                    logger.info(f" БЕРЁМ ИЗ КЭША: {len(cached)} матчей")
                    filtered_matches = cached
                else:
                    logger.info(f" ИДЁМ В API: cached={len(cached)}, update={update}")
                    data = get_matches_by_date(api_date)
                    for match in data.get("response", {}).get("matches", []):
                        if match.get("leagueId") == league_id:
                            filtered_matches.append(match)
                            save_match_from_api(match, league_id, api_date)
                    logger.info(f" ИЗ API ПОЛУЧЕНО: {len(filtered_matches)} матчей")
            else:
                cached = get_matches(league_id, api_date)
                if not cached:
                    data = get_matches_by_date(api_date)
                    for match in data.get("response", {}).get("matches", []):
                        if match.get("leagueId") == league_id:
                            filtered_matches.append(match)
                            save_match_from_api(match, league_id, api_date)
                else:
                    filtered_matches = cached
                    logger.info(f" БЕРЁМ ИЗ КЭША: {len(cached)} матчей")

            if not filtered_matches:
                bot.send_message(chat_id, f"❌ Матчей для {league_name} на {display_date} не найдено.")
                logger.info(f"Матчей для {chat_id}  на дату {display_date} не найдено")
                return False
            logger.info(f"Матчи для {chat_id}  на дату {display_date} показаны")
            bot.send_message(
                chat_id,
                f"⚽ **{league_name} — матчи на {display_date}**\n\nНажмите на матч для подробностей:",
                reply_markup=matches_keyboard(filtered_matches),
                parse_mode="Markdown"
            )
            return True
        except Exception as e:
            logger.debug(f"Ошибка: {e}")
            bot.send_message(chat_id, "API временно не доступен")
        return False


    @bot.callback_query_handler(func=lambda call: call.data.startswith("match_"))
    def handle_match_callback(call):
        match_id = int(call.data.split("_")[1])
        bot.answer_callback_query(call.id)
        chat_id = call.message.chat.id
        try:
            match_info_cache = get_match_by_id(match_id)
            if match_info_cache:
                date_passed = is_match_date_passed(match_info_cache["date"])
                status = match_info_cache["status"]
                if date_passed and status != "FT":
                    logger.info(f"МАТЧ {match_id}: дата прошла, статус {status} != FT, идём в API")
                    cached = None
                    cached_score = None
                else:
                    cached = get_lineup(match_id)
                    if cached and cached.get("home", {}).get("response", {}).get("lineup", {}).get("formation") != '':
                        pass
                    else:
                        cached = None
                    cached_score = get_match_by_id(match_id)
            else:
                logger.info(f"МАТЧ {match_id}: нет в БД, идём в API")
                cached = None
                cached_score = None
            
            if cached is not None and cached_score is not None:
                logger.info(f"МАТЧ {match_id}: БЕРЁМ ИЗ КЭША")
                home_data = cached["home"]
                away_data = cached["away"]
                score = cached_score["score"]
                time = cached_score["time"]
                match_info = {"score": score, "time": time}
            else:
                cached_score = get_match_by_id(match_id)
                if cached_score:
                    match_date = datetime.strptime(match_info_cache["date"], "%Y%m%d")
                    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    days_until = (match_date - today).days
                    if days_until > 1:
                        bot.send_message(chat_id,"Информации по составу для этого матча пока нет.\n" "Попробуйте в день матча — тогда появятся составы команд.")
                        bot.send_message(chat_id, "⬅️ Нажмите 'К матчам', чтобы вернуться", reply_markup=back_to_matches())
                        return
                logger.info(f"МАТЧ {match_id}: ИДЁМ В API (cached={cached is not None}, cached_score={cached_score is not None})")
                home_data, away_data, score_data = get_match_details(match_id)
                score = score_data.get("response", {}).get("status", {}).get("scoreStr", "")
                time = score_data.get("response", {}).get("time", "")
                new_status = score_data.get("response", {}).get("status", {}).get("reason", {}).get("short", "")
                if "message" in score_data or not score_data.get("response"):
                    logger.warning(f"МАТЧ {match_id}: API недоступен")
                    bot.send_message(chat_id, "API временно недоступен")
                    return
                save_match(
                    match_id=match_id,
                    league_id=score_data.get("response", {}).get("leagueId", 0),
                    date=datetime.strptime(time[:10], "%d.%m.%Y").strftime("%Y%m%d") if time else "",
                    home_team=home_data.get("name", ""),
                    away_team=away_data.get("name", ""),
                    score=score,
                    status=new_status,
                    time=time
                )
                home_lineup = home_data.get("response", {}).get("lineup", {})
                away_lineup = away_data.get("response", {}).get("lineup", {})
                save_lineup(
                    match_id=match_id,
                    home_formation=home_lineup.get("formation", ""),
                    home_rating=home_lineup.get("rating", ""),
                    home_starters=home_lineup.get("starters", []),
                    away_formation=away_lineup.get("formation", ""),
                    away_rating=away_lineup.get("rating", ""),
                    away_starters=away_lineup.get("starters", [])
                )
                match_info = {"score": score, "time": time}
                logger.info(f"МАТЧ {match_id}: СОХРАНЁН В БД")
            
            text = format_match_details(home_data, away_data, match_info)
            
            match_after = get_match_by_id(match_id)
            if match_after and match_after["status"] == "FT":
                logger.info(f"МАТЧ {match_id}: статус FT, показываем с кнопкой обзора")
                bot.send_message(chat_id, text, reply_markup=ai_keyboard_for_ended(match_id), parse_mode="Markdown")
                bot.send_message(chat_id, "⬅️ Нажмите 'К матчам', чтобы вернуться", reply_markup=back_to_matches())
            else:
                logger.info(f"МАТЧ {match_id}: статус не FT, показываем с кнопкой прогноза")
                bot.send_message(chat_id, text, reply_markup=ai_keyboard_for_not_stated(match_id), parse_mode="Markdown")
                bot.send_message(chat_id, "⬅️ Нажмите 'К матчам', чтобы вернуться", reply_markup=back_to_matches())
        
        except Exception as e:
            logger.error(f"Ошибка в handle_match_callback для матча {match_id}: {e}", exc_info=True)
            bot.send_message(chat_id, f"❌ Ошибка: {e}")