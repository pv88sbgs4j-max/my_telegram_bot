import json
import os

CACHE_FILE = "data/matches_cache.json"
CACHE_FILE_FOR_LINEUPS = "data/lineups_cache.json"

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

def load_cache_for_lineups():
    if os.path.exists(CACHE_FILE_FOR_LINEUPS):
        with open(CACHE_FILE_FOR_LINEUPS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache_for_lineups(cache):
    os.makedirs(os.path.dirname(CACHE_FILE_FOR_LINEUPS), exist_ok = True)
    with open(CACHE_FILE_FOR_LINEUPS, "w", encoding= "utf-8") as f:
        json.dump(cache, f , indent = 2, ensure_ascii=False)

def get_cached_lineups(match_id):
    cache = load_cache_for_lineups() 
    match_id_str = str(match_id)

    if match_id_str in cache:
        return cache[match_id_str]
    return None

def save_lineups_to_cache(match_id, matches):
    cache = load_cache_for_lineups()
    match_id_str = str(match_id)
    cache[match_id_str] = matches
    save_cache_for_lineups(cache)

def get_score_by_match_id(match_id):
    cache = load_cache()  
    for league_id, dates in cache.items():
        for date, matches in dates.items():
            for match in matches:
                if match.get("id") == match_id:
                    return {
                        "score": match.get("status", {}).get("scoreStr", ""),
                        "time": match.get("time", "")
                    }
    return None

def get_match_date_and_status(match_id):
    cache = load_cache()
    for league_id, dates in cache.items():
        for date, matches in dates.items():
            for match in matches:
                if match.get("id") == match_id:
                    return {
                        "date": match.get("time", ""),  
                        "status": match.get("status", {}).get("reason", {}).get("short", "")
                    }
    return None

def update_match_status_in_cache(match_id, new_status):
    cache = load_cache()
    for league_id, dates in cache.items():
        for date, matches in dates.items():
            for match in matches:
                if match.get("id") == match_id:
                    if "status" not in match:
                        match["status"] = {}
                    if "reason" not in match["status"]:
                        match["status"]["reason"] = {}
                    match["status"]["reason"]["short"] = new_status
                    save_cache(cache)
                    return