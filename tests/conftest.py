import pytest
import database

from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    test_db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", str(test_db_path))
    database.init_db()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_match():
    return {
        "match_id": 12345,
        "league_id": 1,
        "date": "20260822",
        "home_team": "Arsenal",
        "away_team": "Chelsea",
        "score": "3 - 0",
        "status": "FT",
        "time": "22.08.2026 21:00"
    }


@pytest.fixture
def sample_lineup():
    return {
        "home": {
            "response": {
                "lineup": {
                    "name": "Arsenal",
                    "formation": "4-3-3",
                    "rating": "7.2",
                    "starters": [
                        {
                            "id": 1187236,
                            "age": 25,
                            "name": "Carl Rushworth",
                            "positionId": 11,
                            "usualPlayingPositionId": 0,
                            "shirtNumber": "19",
                            "countryName": "England",
                            "countryCode": "ENG",
                            "horizontalLayout": {"x": 0.1, "y": 0.5, "height": 0.25, "width": 0.2},
                            "verticalLayout": {"x": 0.5, "y": 0.1, "height": 0.2, "width": 1},
                            "marketValue": 7201916,
                            "performance": {
                                "rating": 5.9,
                                "fantasyScore": "1",
                                "totalDistanceCovered": 5449,
                                "topSpeed": 23.299999237060547
                            },
                            "firstName": "Carl",
                            "lastName": "Rushworth",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 22, "totalPlayers": 31},
                                "topSpeed": {"rank": 31, "totalPlayers": 31}
                            }
                        },
                        {
                            "id": 1074750,
                            "age": 25,
                            "name": "Milan van Ewijk",
                            "positionId": 32,
                            "usualPlayingPositionId": 1,
                            "shirtNumber": "27",
                            "countryName": "Netherlands",
                            "countryCode": "NED",
                            "horizontalLayout": {"x": 0.357, "y": 0.875, "height": 0.25, "width": 0.257},
                            "verticalLayout": {"x": 0.125, "y": 0.357, "height": 0.2, "width": 0.25},
                            "marketValue": 13233823,
                            "performance": {
                                "rating": 4.3,
                                "fantasyScore": "1",
                                "totalDistanceCovered": 9579,
                                "topSpeed": 34.70000076293945
                            },
                            "firstName": "Milan",
                            "lastName": "van Ewijk",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 11, "totalPlayers": 31},
                                "topSpeed": {"rank": 2, "totalPlayers": 31}
                            }
                        },
                        {
                            "id": 1161885,
                            "age": 25,
                            "name": "Bobby Thomas",
                            "positionId": 34,
                            "usualPlayingPositionId": 1,
                            "shirtNumber": "4",
                            "countryName": "England",
                            "countryCode": "ENG",
                            "horizontalLayout": {"x": 0.357, "y": 0.625, "height": 0.25, "width": 0.257},
                            "verticalLayout": {"x": 0.375, "y": 0.357, "height": 0.2, "width": 0.25},
                            "marketValue": 5838479,
                            "performance": {
                                "rating": 6.5,
                                "fantasyScore": "3",
                                "totalDistanceCovered": 10114,
                                "topSpeed": 30.200000762939453
                            },
                            "firstName": "Bobby",
                            "lastName": "Thomas",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 10, "totalPlayers": 31},
                                "topSpeed": {"rank": 18, "totalPlayers": 31}
                            }
                        },
                        {
                            "id": 1257648,
                            "age": 23,
                            "name": "Aurèle Amenda",
                            "positionId": 36,
                            "usualPlayingPositionId": 1,
                            "shirtNumber": "24",
                            "countryName": "Switzerland",
                            "countryCode": "SUI",
                            "horizontalLayout": {"x": 0.357, "y": 0.375, "height": 0.25, "width": 0.257},
                            "verticalLayout": {"x": 0.625, "y": 0.357, "height": 0.2, "width": 0.25},
                            "marketValue": 7830653,
                            "performance": {
                                "rating": 5.6,
                                "fantasyScore": "1",
                                "totalDistanceCovered": 9511,
                                "topSpeed": 32.599998474121094
                            },
                            "firstName": "Aurèle",
                            "lastName": "Amenda",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 12, "totalPlayers": 31},
                                "topSpeed": {"rank": 5, "totalPlayers": 31}
                            }
                        },
                        {
                            "id": 759814,
                            "age": 28,
                            "name": "Jay Dasilva",
                            "positionId": 38,
                            "usualPlayingPositionId": 1,
                            "shirtNumber": "3",
                            "countryName": "Wales",
                            "countryCode": "WAL",
                            "horizontalLayout": {"x": 0.357, "y": 0.125, "height": 0.25, "width": 0.257},
                            "verticalLayout": {"x": 0.875, "y": 0.357, "height": 0.2, "width": 0.25},
                            "marketValue": 3786668,
                            "performance": {
                                "rating": 5.4,
                                "fantasyScore": "1",
                                "totalDistanceCovered": 10141,
                                "topSpeed": 31.200000762939453
                            },
                            "firstName": "Jay",
                            "lastName": "Dasilva",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 9, "totalPlayers": 31},
                                "topSpeed": {"rank": 14, "totalPlayers": 31}
                            }
                        },
                        {
                            "id": 1615927,
                            "age": 20,
                            "name": "Caleb Yirenkyi",
                            "positionId": 73,
                            "usualPlayingPositionId": 2,
                            "shirtNumber": "8",
                            "countryName": "Ghana",
                            "countryCode": "GHA",
                            "horizontalLayout": {"x": 0.613, "y": 0.79, "height": 0.25, "width": 0.257},
                            "verticalLayout": {"x": 0.21, "y": 0.613, "height": 0.2, "width": 0.29},
                            "marketValue": 5651013,
                            "performance": {
                                "rating": 5.8,
                                "events": [{"type": "yellowCard"}],
                                "substitutionEvents": [
                                    {"time": 62, "type": "subOut", "reason": "tactical"}
                                ],
                                "fantasyScore": "1",
                                "totalDistanceCovered": 7912,
                                "topSpeed": 30.299999237060547
                            },
                            "firstName": "Caleb",
                            "lastName": "Yirenkyi",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 18, "totalPlayers": 31},
                                "topSpeed": {"rank": 17, "totalPlayers": 31}
                            }
                        },
                        {
                            "id": 478357,
                            "age": 31,
                            "name": "Matt Grimes",
                            "positionId": 75,
                            "usualPlayingPositionId": 2,
                            "shirtNumber": "6",
                            "isCaptain": True,
                            "countryName": "England",
                            "countryCode": "ENG",
                            "horizontalLayout": {"x": 0.613, "y": 0.5, "height": 0.25, "width": 0.257},
                            "verticalLayout": {"x": 0.5, "y": 0.613, "height": 0.2, "width": 0.29},
                            "marketValue": 2887922,
                            "performance": {
                                "rating": 6.4,
                                "fantasyScore": "2",
                                "totalDistanceCovered": 11705,
                                "topSpeed": 29.700000762939453
                            },
                            "firstName": "Matt",
                            "lastName": "Grimes",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 2, "totalPlayers": 31},
                                "topSpeed": {"rank": 20, "totalPlayers": 31}
                            }
                        },
                        {
                            "id": 856685,
                            "age": 28,
                            "name": "Frank Onyeka",
                            "positionId": 77,
                            "usualPlayingPositionId": 2,
                            "shirtNumber": "16",
                            "countryName": "Nigeria",
                            "countryCode": "NGA",
                            "horizontalLayout": {"x": 0.613, "y": 0.21, "height": 0.25, "width": 0.257},
                            "verticalLayout": {"x": 0.79, "y": 0.613, "height": 0.2, "width": 0.29},
                            "marketValue": 3980722,
                            "performance": {
                                "rating": 6.2,
                                "fantasyScore": "2",
                                "totalDistanceCovered": 11633,
                                "topSpeed": 31.600000381469727
                            },
                            "firstName": "Frank",
                            "lastName": "Onyeka",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 3, "totalPlayers": 31},
                                "topSpeed": {"rank": 10, "totalPlayers": 31}
                            }
                        },
                        {
                            "id": 1283034,
                            "age": 22,
                            "name": "Loum Tchaouna",
                            "positionId": 103,
                            "usualPlayingPositionId": 3,
                            "shirtNumber": "18",
                            "countryName": "France",
                            "countryCode": "FRA",
                            "horizontalLayout": {"x": 0.87, "y": 0.79, "height": 0.25, "width": 0.257},
                            "verticalLayout": {"x": 0.21, "y": 0.87, "height": 0.2, "width": 0.29},
                            "marketValue": 17698651,
                            "performance": {
                                "rating": 6.2,
                                "substitutionEvents": [
                                    {"time": 82, "type": "subOut", "reason": "tactical"}
                                ],
                                "fantasyScore": "2",
                                "totalDistanceCovered": 9419,
                                "topSpeed": 33.5
                            },
                            "firstName": "Loum",
                            "lastName": "Tchaouna",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 14, "totalPlayers": 31},
                                "topSpeed": {"rank": 3, "totalPlayers": 31}
                            }
                        },
                        {
                            "id": 982284,
                            "age": 25,
                            "name": "Ellis Simms",
                            "positionId": 105,
                            "usualPlayingPositionId": 3,
                            "shirtNumber": "9",
                            "countryName": "England",
                            "countryCode": "ENG",
                            "horizontalLayout": {"x": 0.87, "y": 0.5, "height": 0.25, "width": 0.257},
                            "verticalLayout": {"x": 0.5, "y": 0.87, "height": 0.2, "width": 0.29},
                            "marketValue": 8385079,
                            "performance": {
                                "rating": 6.5,
                                "substitutionEvents": [
                                    {"time": 70, "type": "subOut", "reason": "tactical"}
                                ],
                                "fantasyScore": "2",
                                "totalDistanceCovered": 7702,
                                "topSpeed": 29.5
                            },
                            "firstName": "Ellis",
                            "lastName": "Simms",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 19, "totalPlayers": 31},
                                "topSpeed": {"rank": 21, "totalPlayers": 31}
                            }
                        },
                        {
                            "id": 776184,
                            "age": 27,
                            "name": "Brandon Thomas-Asante",
                            "positionId": 107,
                            "usualPlayingPositionId": 3,
                            "shirtNumber": "23",
                            "countryName": "Ghana",
                            "countryCode": "GHA",
                            "horizontalLayout": {"x": 0.87, "y": 0.21, "height": 0.25, "width": 0.257},
                            "verticalLayout": {"x": 0.79, "y": 0.87, "height": 0.2, "width": 0.29},
                            "marketValue": 5498706,
                            "performance": {
                                "rating": 6.1,
                                "substitutionEvents": [
                                    {"time": 70, "type": "subOut", "reason": "tactical"}
                                ],
                                "fantasyScore": "2",
                                "totalDistanceCovered": 8222,
                                "topSpeed": 31.700000762939453
                            },
                            "firstName": "Brandon",
                            "lastName": "Thomas-Asante",
                            "rankings": {
                                "totalDistanceCovered": {"rank": 16, "totalPlayers": 31},
                                "topSpeed": {"rank": 9, "totalPlayers": 31}
                            }
                        }
                    ]
                }
            }
        },
        "away": {
            "response": {
                "lineup": {
                    "name": "Chelsea",
                    "formation": "4-2-3-1",
                    "rating": "6.8",
                    "starters": []
                }
            }
        }
    }