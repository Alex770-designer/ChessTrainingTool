import re
import requests
import chess.pgn
import io


def extract_game_id(game_url):
    """
    Extract the Lichess game ID from a game URL.
    """

    match = re.search(
        r"lichess\.org/([A-Za-z0-9]+)",
        game_url
    )

    if not match:
        raise ValueError(
            "Invalid Lichess game URL."
        )

    return match.group(1)


def get_lichess_game(game_url):
    """
    Download a specific Lichess game as PGN.
    """

    game_id = extract_game_id(game_url)

    url = (
        f"https://lichess.org/game/export/"
        f"{game_id}"
    )

    headers = {
        "Accept": "application/x-chess-pgn"
    }

    response = requests.get(
        url,
        headers=headers
    )

    if response.status_code != 200:
        raise ValueError(
            f"Could not retrieve Lichess game. "
            f"Status code: {response.status_code}"
        )

    return response.text
