import sqlite3
import json
from datetime import datetime
from typing import Optional


DB_PATH = "bot_cache.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY,
            league_id INTEGER,
            date TEXT,
            home_team TEXT,
            away_team TEXT,
            score TEXT,
            status TEXT,
            time TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lineups (
            match_id INTEGER PRIMARY KEY,
            home_formation TEXT,
            home_rating TEXT,
            home_starters TEXT,
            away_formation TEXT,
            away_rating TEXT,
            away_starters TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction (
        match_id INTEGER PRIMARY KEY,
        prediction TEXT)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS review (
        match_id INTEGER PRIMARY KEY,
        review TEXT)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_state (
        chat_id INTEGER PRIMARY KEY,
        last_league TEXT,
        last_api_date TEXT,
        last_display_date TEXT,
        updated_at TEXT)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checked_dates (
        league_id INTEGER,
        date TEXT,
        checked_at TEXT,
        PRIMARY KEY (league_id, date))
        """)
    
    conn.commit()
    conn.close()


def save_user_state(chat_id:int, league:str, api_date:str, display_date:str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO user_state (chat_id, last_league, last_api_date, last_display_date, updated_at)
        VALUES (? , ? , ? , ? , ?)
        """, (chat_id, league, api_date, display_date, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_user_state(chat_id:int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_state WHERE chat_id = ?", (chat_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "chat_id": row[0],
            "last_league": row[1],
            "last_api_date": row[2],
            "last_display_date": row[3]
        }
    return None


def save_prediction(match_id:int,prediction:str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO prediction (match_id, prediction)
        VALUES (? , ?)
        """, (match_id, prediction))
    conn.commit()
    conn.close()


def get_prediction(match_id:int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM prediction WHERE match_id = ?
        """, (match_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "match_id": row[0],
            "prediction": row[1]
        }
    return None


def save_review(match_id:int,review:str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO review (match_id, review)
        VALUES (? , ?)
        """, (match_id, review))
    conn.commit()
    conn.close()


def get_review(match_id:int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM review WHERE match_id = ?
        """, (match_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "match_id": row[0],
            "review": row[1]
        }
    return None


def save_match(match_id:int, league_id:int, date:str, home_team:str, away_team:str, score:str, status:str, time:str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO matches (match_id, league_id, date, home_team, away_team, score, status, time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (match_id, league_id, date, home_team, away_team, score, status, time))
    conn.commit()
    conn.close()

def get_matches(league_id: int, date: str) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT match_id, league_id, date, home_team, away_team, score, status, time 
        FROM matches WHERE league_id = ? AND date = ?
    """, (league_id, date))
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "match_id": row[0],
            "league_id": row[1],
            "date": row[2],
            "home_team": row[3],       
            "away_team": row[4],      
            "score": row[5],
            "status": row[6],        
            "time": row[7]
        }
        for row in rows
    ]


def get_match_by_id(match_id:int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matches WHERE match_id = ?", (match_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "leagueId": row[1],
            "date": row[2],
            "home_team": row[3],
            "away_team": row[4],
            "score": row[5],
            "status": row[6],
            "time": row[7]
        }
    return None


def save_lineup(match_id:int, home_formation:str, home_rating:str, home_starters:list, away_formation:str, away_rating:str, away_starters:list) -> None:
    home_starters_json = json.dumps(home_starters)
    away_starters_json = json.dumps(away_starters)
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO lineups (match_id, home_formation, home_rating, home_starters, away_formation, away_rating, away_starters)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (match_id, home_formation, home_rating, home_starters_json, away_formation, away_rating, away_starters_json))
    conn.commit()
    conn.close()

def get_lineup(match_id:int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            m.home_team, m.away_team,
            l.home_formation, l.home_rating, l.home_starters,
            l.away_formation, l.away_rating, l.away_starters
        FROM matches m
        LEFT JOIN lineups l ON m.match_id = l.match_id
        WHERE m.match_id = ?
    """, (match_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        import json
        home_starters = json.loads(row[4]) if row[4] else []
        away_starters = json.loads(row[7]) if row[7] else []
        
        return {
            "home": {
                "response": {
                    "lineup": {
                        "name": row[0] or "Команда 1",
                        "formation": row[2] or "",
                        "rating": row[3] or "",
                        "starters": home_starters
                    }
                }
            },
            "away": {
                "response": {
                    "lineup": {
                        "name": row[1] or "Команда 2",
                        "formation": row[5] or "",
                        "rating": row[6] or "",
                        "starters": away_starters
                    }
                }
            }
        }
    return None


def save_match_from_api(match:dict, league_id:int, api_date:str) -> None:
    save_match(
        match_id=match.get("id"),
        league_id=league_id,
        date=api_date,
        home_team=match.get("home", {}).get("name", ""),
        away_team=match.get("away", {}).get("name", ""),
        score=match.get("status", {}).get("scoreStr", ""),
        status=match.get("status", {}).get("reason", {}).get("short", ""),
        time=match.get("time", "")
        )


def is_date_checked(league_id: int, date: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM checked_dates WHERE league_id = ? AND date = ?",
        (league_id, date)
    )
    result = cursor.fetchone() is not None
    conn.close()
    return result


def mark_date_checked(league_id: int, date: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO checked_dates (league_id, date, checked_at)
        VALUES (?, ?, ?)
    """, (league_id, date, datetime.now().isoformat()))
    conn.commit()
    conn.close()