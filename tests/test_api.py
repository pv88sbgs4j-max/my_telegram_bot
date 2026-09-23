from database import save_match

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_matches_empty(client):
    response = client.get("/matches_by_date?league_id=999&date=20990101")
    assert response.status_code == 404 
    assert response.json()["detail"] == "Matches not found"


def test_get_match_by_id(client, sample_match):
    save_match(**sample_match)

    match_id = sample_match["match_id"] 
    response = client.get(f"/matches/{match_id}")

    assert response.status_code == 200
    assert response.json()["home_team"] == "Arsenal"