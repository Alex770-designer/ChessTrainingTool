from flask import Flask, jsonify, request
from flask_cors import CORS
from main import analyze_pgn
import json
import random
import os
from imports.chesscom import get_chesscom_game
from puzzle_generator import generate_puzzles
from imports.lichess import get_lichess_game


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ANALYSIS_PATH = os.path.join(
    BASE_DIR,
    "analysis.json"
)

PUZZLES_PATH = os.path.join(
    BASE_DIR,
    "puzzles.json"
)


app = Flask(__name__)

CORS(app)


@app.route("/upload", methods=["POST"])
def upload_game():

    data = request.get_json()

    pgn = data.get("pgn", "")

    if not pgn:
        return jsonify({
            "message": "No PGN provided.",
            "moves_analyzed": 0,
            "puzzles_created": 0
        }), 400

    try:

        # Analyze the uploaded game
        results = analyze_pgn(pgn)

        # Generate puzzles from analyzed moves
        puzzles = []

        for move in results:

            if abs(move["loss"]) >= 100:

                puzzles.append({
                    "fen": move["fen"],
                    "solution": move["best_line"],
                    "category": move["category"],
                    "reason": move["reason"]
                })

        # Save puzzles
        with open(PUZZLES_PATH, "w") as file:
            json.dump(
                puzzles,
                file,
                indent=4
            )

        return jsonify({
            "message": "Game analyzed successfully!",
            "moves_analyzed": len(results),
            "puzzles_created": len(puzzles)
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "message": "Error analyzing game.",
            "error": str(e),
            "moves_analyzed": 0,
            "puzzles_created": 0
        }), 500


@app.route("/puzzles")
def get_puzzles():

    if not os.path.exists(PUZZLES_PATH):
        return jsonify({
            "puzzles": []
        })

    with open(PUZZLES_PATH, "r") as file:
        puzzles = json.load(file)

    return jsonify({
        "puzzles": puzzles
    })


@app.route("/analysis")
def get_analysis():

    if not os.path.exists(ANALYSIS_PATH):
        return jsonify({
            "analysis": []
        })

    with open(ANALYSIS_PATH, "r") as file:
        analysis = json.load(file)

    return jsonify({
        "analysis": analysis
    })

@app.route("/import-chess-com", methods=["POST"])
def import_chess_com():

    try:
        data = request.get_json()

        username = data.get("username")
        date = data.get("date")
        game_url = data.get("game_url")

        if not username or not date or not game_url:
            return jsonify({
                "message": "Username, date, and game URL are required."
            }), 400

        # Date format: YYYY-MM-DD
        year, month, day = date.split("-")

        pgn = get_chesscom_game(
            username,
            int(year),
            int(month),
            game_url
        )

        # Analyze the retrieved game
        result = analyze_pgn(pgn)

        # Generate puzzles from the new analysis
        puzzles = generate_puzzles()

        return jsonify({
            "message": "Chess.com game imported successfully.",
            "moves_analyzed": len(result),
            "puzzles_created": len(puzzles)
        })

    except Exception as e:

        print("Chess.com import error:", e)

        return jsonify({
            "message": f"Error importing Chess.com game: {str(e)}"
        }), 500

@app.route("/import-lichess", methods=["POST"])
def import_lichess():

    try:
        data = request.get_json()

        game_url = data.get("game_url")

        if not game_url:
            return jsonify({
                "message": "Lichess game URL is required."
            }), 400

        pgn = get_lichess_game(game_url)

        result = analyze_pgn(pgn)

        puzzles = generate_puzzles()

        return jsonify({
            "message": "Lichess game imported successfully.",
            "moves_analyzed": len(result),
            "puzzles_created": len(puzzles)
        })

    except Exception as e:

        print("Lichess import error:", e)

        return jsonify({
            "message": f"Error importing Lichess game: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)