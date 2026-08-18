import chess
import chess.pgn
from analysis import ChessAnalysis
import json
import io
import os
from phase_detector import classify_analysis


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_PATH = os.path.join(BASE_DIR, "analysis.json")

def detect_player_color(game, username=None):
    """
    Determine whether the user is playing White or Black.
    """

    white = game.headers.get("White", "")
    black = game.headers.get("Black", "")

    if username:
        username = username.lower()

        if white.lower() == username:
            return "white"

        if black.lower() == username:
            return "black"

    return None

def generate_move_reason(
    board,
    move,
    best_line,
    material_loss,
    loss
):
    """
    Generate a more specific explanation for why a move was inaccurate.
    """

    tactical_reason = detect_tactical_reason(
        board,
        move,
        best_line
    )

    if tactical_reason and loss >= 100:
        return tactical_reason

    # Good move
    if loss < 100:
        return "This move was slightly less accurate than the best option."

    # Material loss
    if material_loss >= 300:
        return "This move resulted in a significant material loss."

    if material_loss >= 100:
        return "This move resulted in a noticeable material loss."

    # Missed best move
    if best_line:
        best_move = best_line[0]

        if move != best_move:
            try:
                best_move_san = board.san(best_move)

                if loss >= 500:
                    return (
                        f"This move caused a major deterioration "
                        f"in the position. Stockfish preferred "
                        f"{best_move_san}."
                    )

                if loss >= 300:
                    return (
                        f"This move significantly worsened the position. "
                        f"Stockfish preferred {best_move_san}."
                    )

                if loss >= 150:
                    return (
                        f"This move gave up a noticeable advantage. "
                        f"Stockfish preferred {best_move_san}."
                    )

                return (
                    f"This move missed a stronger opportunity. "
                    f"Stockfish preferred {best_move_san}."
                )

            except Exception:
                pass

    return "This move was less accurate than the best option."

def detect_tactical_reason(board, move, best_line):
    """
    Detect simple tactical patterns from the current position.
    """

    # If Stockfish has no recommendation, we cannot compare.
    if not best_line:
        return None

    best_move = best_line[0]

    # The played move wasn't the engine's preferred move.
    if move == best_move:
        return None

    # --------------------------------------------------
    # Missed capture
    # --------------------------------------------------

    if board.is_capture(best_move) and not board.is_capture(move):

        try:
            captured_piece = board.piece_at(best_move.to_square)

            if captured_piece:
                piece_name = {
                    chess.PAWN: "pawn",
                    chess.KNIGHT: "knight",
                    chess.BISHOP: "bishop",
                    chess.ROOK: "rook",
                    chess.QUEEN: "queen",
                    chess.KING: "king"
                }.get(
                    captured_piece.piece_type,
                    "piece"
                )

                return (
                    f"You missed an opportunity to capture "
                    f"the opponent's {piece_name}."
                )

        except Exception:
            pass

    # --------------------------------------------------
    # Missed check
    # --------------------------------------------------

    if board.gives_check(best_move) and not board.gives_check(move):

        return (
            "You missed a stronger checking move that "
            "could have created a tactical opportunity."
        )

    return None

def analyze_pgn(pgn_text, username=None, player_color=None):

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

    white_player = game.headers.get("White", "Unknown")
    black_player = game.headers.get("Black", "Unknown")

    if player_color is None:
        player_color = detect_player_color(
            game,
            username
        )

    if player_color is None:
        player_color = "white"


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
        reason = generate_move_reason(
            board,
            move,
            best_line,
            material_loss,
            loss
        )

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
            "reason": reason, 
            "player_color": player_color,
        })

        board.push(move)

    analysis.close()

    results = classify_analysis(results)

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