from fastapi import FastAPI , HTTPException
from database import get_matches , get_lineup, get_match_by_id


app = FastAPI(title="Football Bot API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/matches_by_date")
def matches(league_id, date):
    m = get_matches(league_id, date)
    if not m:
        raise HTTPException(status_code=404, detail = "Matches not found")
    return m


@app.get("/lineups")
def matches(match_id):
    m = get_lineup(match_id)
    if not m:
        raise HTTPException(status_code=404, detail = "Lineup not found")
    return m

@app.get("/match_by_id")
def match_by_id(match_id):
    m = get_match_by_id(match_id)
    if not m:
        raise HTTPException(status_code=404, detail = "Match not found")
    return m