import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ANALYSIS_PATH = os.path.join(BASE_DIR, "analysis.json")
PUZZLES_PATH = os.path.join(BASE_DIR, "puzzles.json")


def generate_puzzles():

    with open(ANALYSIS_PATH) as file:
        games = json.load(file)

    puzzles = []

    for move in games:

        if abs(move["loss"]) >= 100:

            puzzles.append({
                "fen": move["fen"],
                "solution": move["best_move"],
                "category": move["category"],
                "reason": move["reason"]
            })


    with open(PUZZLES_PATH, "w") as file:
        json.dump(puzzles, file, indent=4)


    return puzzles