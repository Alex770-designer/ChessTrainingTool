import requests

response = requests.post(
    "http://127.0.0.1:5000/import-chess-com",
    json={
        "username": "s137340",
        "date": "2025-12-08",
        "game_url": "https://www.chess.com/game/live/146479328270"
    }
)

print("Status:", response.status_code)
print("Response:", response.json())