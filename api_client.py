import requests
from config import headers

def get_match_details(match_id):
    url_home = "https://free-api-live-football-data.p.rapidapi.com/football-get-hometeam-lineup"
    querystring_home = {"eventid": match_id}
    response_home = requests.get(url_home, headers=headers, params=querystring_home)
    home_data = response_home.json()
    
    url_away = "https://free-api-live-football-data.p.rapidapi.com/football-get-awayteam-lineup"
    querystring_away = {"eventid": match_id}
    response_away = requests.get(url_away, headers=headers, params=querystring_away)
    away_data = response_away.json()
    
    return home_data, away_data


