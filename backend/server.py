from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import os
import chess.pgn
import io
from main import analyze_pgn
from puzzle_generator import generate_puzzles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUZZLES_PATH = os.path.join(BASE_DIR, "puzzles.json")
ANALYSIS_PATH = os.path.join(BASE_DIR, "analysis.json")

app = Flask(__name__)

CORS(app)

puzzle_queue = []

@app.route("/puzzle")
def get_puzzle():

    global puzzle_queue

    if len(puzzle_queue) == 0:

        with open(PUZZLES_PATH, "r") as file:
            puzzles = json.load(file)

        puzzle_queue = puzzles.copy()
        random.shuffle(puzzle_queue)

    puzzle = puzzle_queue.pop()

    return {
        "fen": puzzle["fen"],
        "solution": puzzle["solution"],
        "category": puzzle["category"],
        "reason": puzzle["reason"]
    }

@app.route("/upload", methods=["POST"])
def upload_game():

    data = request.json

    pgn = data["pgn"]

    results = analyze_pgn(pgn)

    puzzles = generate_puzzles()

    return {
        "message": "Game analyzed and puzzles created",
        "moves_analyzed": len(results),
        "puzzles_created": len(puzzles)
    }

@app.route("/puzzles")
def get_puzzles():

    with open(PUZZLES_PATH, "r") as file:
        puzzles = json.load(file)

    return {
        "puzzles": puzzles
    }

@app.route("/analysis")
def get_analysis():

    with open(ANALYSIS_PATH, "r") as file:
        analysis = json.load(file)

    return jsonify(analysis)

if __name__ == "__main__":
    app.run(debug=True)