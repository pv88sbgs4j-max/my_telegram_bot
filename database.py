import sqlite3
import json

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
    
    conn.commit()
    conn.close()


def save_match(match_id, league_id, date, home_team, away_team, score, status, time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO matches (match_id, league_id, date, home_team, away_team, score, status, time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (match_id, league_id, date, home_team, away_team, score, status, time))
    conn.commit()
    conn.close()

def get_matches(league_id, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM matches WHERE league_id = ? AND date = ?
    """, (league_id, date))
    rows = cursor.fetchall()
    conn.close()

    matches = []
    for row in rows:
        matches.append({
            "match_id": row[0],
            "league_id": row[1],
            "date": row[2],
            "home_team": {"name": row[3]},
            "away_team": {"name": row[4]},
            "status": {"scoreStr": row[5], "reason": {"short": row[6]}},
            "time": row[7]
        })
    return matches


def get_match_by_id(match_id):
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


def save_lineup(match_id, home_formation, home_rating, home_starters, away_formation, away_rating, away_starters):
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

def get_lineup(match_id):
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

