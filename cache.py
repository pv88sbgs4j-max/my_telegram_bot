import json
import os

CACHE_FILE = "data/matches_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok = True)
    with open(CACHE_FILE, "w", encoding= "utf-8") as f:
        json.dump(cache, f , indent = 2, ensure_ascii=False)

def get_cached_matches(leaugue_id, date):
    cache = load_cache() 
    leaugue_id_str = str(leaugue_id)

    if leaugue_id_str in cache and date in cache[leaugue_id_str]:
        return cache[leaugue_id_str][date]
    return None

def save_matches_to_cache(league_id, date, matches):
    cache = load_cache()
    league_id_str = str(league_id)
    
    if league_id_str not in cache:
        cache[league_id_str] = {}
    cache[league_id_str][date] = matches
    save_cache(cache)   