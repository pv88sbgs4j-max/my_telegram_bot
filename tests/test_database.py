from database import save_match
from database import get_match_by_id
from database import save_lineup
from database import get_lineup


def test_save_and_get_match(sample_match):
    save_match(**sample_match)
    
    result = get_match_by_id(sample_match["match_id"])
    
    assert result is not None
    assert result["home_team"] == "Arsenal"
    assert result["away_team"] == "Chelsea"
    assert result["score"] == "3 - 0"


def test_save_and_get_lineups(sample_lineup,sample_match):

    save_match(**sample_match)

    home_lineup = sample_lineup["home"]["response"]["lineup"]
    away_lineup = sample_lineup["away"]["response"]["lineup"]


    save_lineup(
        match_id=sample_match["match_id"],
        home_formation=home_lineup["formation"],
        home_rating=home_lineup["rating"],
        home_starters=home_lineup["starters"],
        away_formation=away_lineup["formation"],
        away_rating=away_lineup["rating"],
        away_starters=away_lineup["starters"]
    )

    result = get_lineup(sample_match["match_id"])

    assert result is not None

    home_result = result["home"]["response"]["lineup"]
    assert home_result["name"] == "Arsenal"
    assert home_result["formation"] == "4-3-3"
    assert home_result["rating"] == "7.2"
    assert len(home_result["starters"]) == 11

    away_result = result["away"]["response"]["lineup"]
    assert away_result["name"] == "Chelsea"
    assert away_result["formation"] == "4-2-3-1"
    assert away_result["rating"] == "6.8"
    assert away_result["starters"] == []

def test_get_starters(sample_lineup,sample_match):

    save_match(**sample_match)
    
    home_lineup = sample_lineup["home"]["response"]["lineup"]
    away_lineup = sample_lineup["away"]["response"]["lineup"]
    
    
    save_lineup(
        match_id=sample_match["match_id"],
        home_formation=home_lineup["formation"],
        home_rating=home_lineup["rating"],
        home_starters=home_lineup["starters"],
        away_formation=away_lineup["formation"],
        away_rating=away_lineup["rating"],
        away_starters=away_lineup["starters"]
        )
    
    result = get_lineup(sample_match["match_id"])

    starters = result["home"]["response"]["lineup"]["starters"]
    first = starters[0]

    assert first["id"] == 1187236
    assert first["name"] == "Carl Rushworth"
    assert first["age"] == 25
    assert first["shirtNumber"] == "19"
    assert first["countryName"] == "England"
    assert first["performance"]["rating"] == 5.9
    assert first["performance"]["totalDistanceCovered"] == 5449
    assert first["rankings"]["topSpeed"]["rank"] == 31
