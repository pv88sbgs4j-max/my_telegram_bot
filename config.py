import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

LEAGUE_NAME_TICKER = {
    "EPL🏴󠁧󠁢󠁥󠁮󠁧󠁿": "EPL",
    "LALIGA🇪🇸": "LALIGA",
    "BUNDES🇩🇪": "BUNDES"
}

LEAGUE_IDS = {
    "EPL🏴󠁧󠁢󠁥󠁮󠁧󠁿": 47,
    "LALIGA🇪🇸": 87,    
    "BUNDES🇩🇪": 54     
}

url = "https://free-api-live-football-data.p.rapidapi.com/football-get-matches-by-date"
url_for_score = "https://free-api-live-football-data.p.rapidapi.com/football-get-match-detail"

API_KEY = os.getenv("API_KEY")
API_HOST = "free-api-live-football-data.p.rapidapi.com"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

headers = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": API_HOST,
	"Content-Type": "application/json"
}
