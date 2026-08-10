import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ANALYSIS_PATH = os.path.join(
    BASE_DIR,
    "analysis.json"
)

PUZZLES_PATH = os.path.join(
    BASE_DIR,
    "puzzles.json"
)


def generate_puzzles():

    with open(ANALYSIS_PATH) as file:
        games = json.load(file)

    puzzles = []

    for move in games:

        if abs(move["loss"]) >= 100:

            loss = abs(move["loss"])
            material_loss = move.get("material_loss", 0)

            if material_loss >= 300:
                reason = "This move resulted in a significant material loss."

            elif material_loss >= 100:
                reason = "This move resulted in a noticeable material loss."

            elif loss >= 500:
                reason = "This move caused a major deterioration in the position."

            elif loss >= 300:
                reason = "This move significantly worsened the position."

            elif loss >= 150:
                reason = "This move gave the opponent a noticeable advantage."

            else:
                reason = "This move missed a stronger opportunity."

            puzzles.append({
                "fen": move["fen"],
                "solution": move["best_line"],
                "player_color": (
                    "white"
                    if " w " in move["fen"]
                    else "black"
                ),
                "category": move["category"],
                "reason": reason
            })


    with open(PUZZLES_PATH, "w") as file:
        json.dump(
            puzzles,
            file,
            indent=4
        )


    return puzzles


if __name__ == "__main__":

    puzzles = generate_puzzles()

    print(f"Generated {len(puzzles)} puzzles!")