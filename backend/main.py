import chess
import chess.pgn
from analysis import ChessAnalysis
import json
import io
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_PATH = os.path.join(BASE_DIR, "analysis.json")


def analyze_pgn(pgn_text):

    results = []

    analysis = ChessAnalysis(
        os.path.join(BASE_DIR, "stockfish", "stockfish.exe")
    )

    game = chess.pgn.read_game(
        io.StringIO(pgn_text)
    )

    if game is None:
        analysis.close()
        return []

    board = game.board()

    for move in game.mainline_moves():

        beforePos = analysis.evaluate_position(board)

        best_line = analysis.best_line(board)

        temp_board = board.copy()
        temp_board.push(move)

        after = analysis.evaluate_position(temp_board)

        material_loss = analysis.piece_value_loss(
            board,
            temp_board
        )

        # Calculate loss BEFORE using it
        if board.turn == chess.WHITE:
            loss = beforePos - after
        else:
            loss = after - beforePos

        # Now generate the explanation
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

        elif loss >= 100:
            reason = "This move missed a stronger opportunity."

        else:
            reason = "This move was slightly less accurate than the best option."

        category = analysis.classify_move(loss)

        results.append({
            "move_number": board.fullmove_number,
            "fen": board.fen(),
            "move": board.san(move),
            "best_move": board.san(best_line[0]),
            "best_line": [str(m) for m in best_line],
            "before_evaluation": beforePos,
            "after_evaluation": after,
            "loss": loss,
            "category": category,
            "reason": reason
        })

        board.push(move)

    analysis.close()

    with open(ANALYSIS_PATH, "w") as file:
        json.dump(results, file, indent=4)

    return results


if __name__ == "__main__":

    sample_path = os.path.join(
        BASE_DIR,
        "games",
        "sample.pgn"
    )

    with open(sample_path) as file:
        pgn = file.read()

    result = analyze_pgn(pgn)

    print(f"Analyzed {len(result)} moves")