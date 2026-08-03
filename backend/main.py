import chess
import chess.pgn
from analysis import ChessAnalysis
import json
import io


def analyze_pgn(pgn_text):

    results = []

    analysis = ChessAnalysis("stockfish/stockfish.exe")

    game = chess.pgn.read_game(
        io.StringIO(pgn_text)
    )

    if game is None:
        analysis.close()
        return []


    board = game.board()


    for move in game.mainline_moves():

        beforePos = analysis.evaluate_position(board)

        best = analysis.best_move(board)

        temp_board = board.copy()
        temp_board.push(move)

        after = analysis.evaluate_position(temp_board)

        material_loss = analysis.piece_value_loss(
            board,
            temp_board
        )


        if material_loss >= 300:
            reason = "Lost a piece"

        elif material_loss > 100:
            reason = "Major evaluation mistake"

        elif material_loss > 0:
            reason = "Small mistake"

        else:
            reason = "No material loss"


        loss = beforePos - after

        category = analysis.classify_move(loss)


        results.append({
            "move_number": board.fullmove_number,
            "fen": board.fen(),
            "move": board.san(move),
            "best_move": str(best),
            "loss": loss,
            "category": category,
            "reason": reason
        })


        board.push(move)


    analysis.close()


    with open("analysis.json", "w") as file:
        json.dump(results, file, indent=4)


    return results