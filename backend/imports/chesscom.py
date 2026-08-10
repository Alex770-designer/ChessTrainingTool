import re
import requests
import chess.pgn
import io


def extract_game_id(game_url):
    """
    Extract the Chess.com game ID from a game URL.
    """

    match = re.search(
        r"/game/(?:live|daily)/(\d+)",
        game_url
    )

    if not match:
        raise ValueError(
            "Invalid Chess.com game URL."
        )

    return match.group(1)


def get_monthly_pgn(username, year, month):
    """
    Download a player's Chess.com monthly PGN archive.
    """

    url = (
        f"https://api.chess.com/pub/player/"
        f"{username}/games/{year}/{month:02d}/pgn"
    )

    headers = {
        "User-Agent": "ChessTrainingTool/1.0"
    }

    response = requests.get(
        url,
        headers=headers
    )

    if response.status_code != 200:
        raise ValueError(
            f"Could not retrieve Chess.com games. "
            f"Status code: {response.status_code}"
        )

    return response.text

def find_game_in_pgn(pgn_text, game_id):
    """
    Find a specific Chess.com game inside
    a monthly PGN archive.
    """

    pgn_stream = io.StringIO(pgn_text)

    while True:

        game = chess.pgn.read_game(pgn_stream)

        if game is None:
            break

        headers = game.headers

        link = headers.get("Link", "")

        if game_id in link:
            return game

    return None


def get_chesscom_game(
    username,
    year,
    month,
    game_url
):
    """
    Retrieve a specific Chess.com game
    and return its PGN text.
    """

    game_id = extract_game_id(game_url)

    monthly_pgn = get_monthly_pgn(
        username,
        year,
        month
    )

    game = find_game_in_pgn(
        monthly_pgn,
        game_id
    )

    if game is None:
        raise ValueError(
            f"Game {game_id} was not found in "
            f"{username}'s "
            f"{year}-{month:02d} archive."
        )

    exporter = chess.pgn.StringExporter(
        headers=True,
        variations=True,
        comments=True
    )

    return game.accept(exporter)
