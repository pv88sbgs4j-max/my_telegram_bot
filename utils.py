from datetime import datetime

def get_today_date() -> str:
    return datetime.now().strftime("%Y%m%d")

def format_players(players):
    text = ""
    for player in players:
        name = player.get("name", "?")
        number = player.get("shirtNumber", "—")
        rating = player.get("performance", {}).get("rating", {})
        text += f"  • #{number} {name} 📈{rating}\n"
    return text


def format_match_details(home_data, away_data, match_info = None):

    if isinstance(match_info, str):
        match_info = {}
    
    home_response = home_data.get("response", {})
    away_response = away_data.get("response", {})
    
    home_lineup = home_response.get("lineup", {})
    away_lineup = away_response.get("lineup", {})
    
    home_name = home_lineup.get("name", "Команда 1")
    home_formation = home_lineup.get("formation", "не указана")
    home_rating = home_lineup.get("rating", "?")
    
    away_name = away_lineup.get("name", "Команда 2")
    away_formation = away_lineup.get("formation", "не указана")
    away_rating = away_lineup.get("rating", "?")

    
    text = f"⚽ **{home_name} 🆚 {away_name}**\n\n"

    if match_info and match_info.get("score"):
        text += f"📊 **Счёт:** {match_info['score']}\n"
        if match_info.get("time"):
            text += f"🕐 {match_info['time']}\n"
        text += "\n"
    
    text += f"🏠 **{home_name}** (рейтинг: {home_rating})\n"
    text += f"📋 Схема: {home_formation}\n\n"
    
    text += f"✈️ **{away_name}** (рейтинг: {away_rating})\n"
    text += f"📋 Схема: {away_formation}\n\n"
    
    home_starters = home_lineup.get("starters", [])
    away_starters = away_lineup.get("starters", [])
    
    if home_starters:
        text += f"🏠 **Стартовый состав {home_name}:**\n"
        text += format_players(home_starters)
        text += "\n"
    
    if away_starters:
        text += f"✈️ **Стартовый состав {away_name}:**\n"
        text += format_players(away_starters)
    
    return text
