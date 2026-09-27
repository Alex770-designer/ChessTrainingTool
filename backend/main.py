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
    Generate a specific explanation and machine-readable
    reason type for a move.
    """

    # -----------------------------------------
    # Tactical detection
    # -----------------------------------------

    tactical_reason = detect_tactical_reason(
        board,
        move,
        best_line
    )

    if tactical_reason and loss >= 100:

        if "capture" in tactical_reason.lower():
            reason_type = "MISSED_CAPTURE"

        elif "checking move" in tactical_reason.lower():
            reason_type = "MISSED_CHECK"

        elif "promote" in tactical_reason.lower():
            reason_type = "MISSED_PROMOTION"

        else:
            reason_type = "TACTICAL_OPPORTUNITY"

        return tactical_reason, reason_type

    # -----------------------------------------
    # Hanging piece
    # -----------------------------------------

    hanging_reason = detect_hanging_piece(
        board,
        move
    )

    if hanging_reason and loss >= 100:

        return (
            hanging_reason,
            "HANGING_PIECE"
        )

    # -----------------------------------------
    # Fork
    # -----------------------------------------

    fork_reason = detect_fork(
        board,
        move
    )

    if fork_reason and loss >= 100:

        return (
            fork_reason,
            "FORK"
        )

    # -----------------------------------------
    # Material loss
    # -----------------------------------------

    if material_loss >= 300:

        return (
            "This move resulted in a significant material loss.",
            "SIGNIFICANT_MATERIAL_LOSS"
        )

    if material_loss >= 100:

        return (
            "This move resulted in a noticeable material loss.",
            "MATERIAL_LOSS"
        )

    # -----------------------------------------
    # Evaluation loss
    # -----------------------------------------

    if loss >= 500:

        return (
            "This move caused a major deterioration in the position.",
            "MAJOR_EVALUATION_LOSS"
        )

    if loss >= 300:

        return (
            "This move significantly worsened the position.",
            "SIGNIFICANT_EVALUATION_LOSS"
        )

    if loss >= 150:

        if best_line:

            try:

                best_move_san = board.san(
                    best_line[0]
                )

                return (
                    f"This move gave up a noticeable advantage. "
                    f"Stockfish preferred {best_move_san}.",
                    "MISSED_OPPORTUNITY"
                )

            except Exception:
                pass

        return (
            "This move gave up a noticeable advantage.",
            "MISSED_OPPORTUNITY"
        )

    # -----------------------------------------
    # Inaccuracy
    # -----------------------------------------

    return (
        "This move was slightly less accurate than the best option.",
        "INACCURACY"
    )

def detect_tactical_reason(board, move, best_line):
    """
    Detect simple tactical patterns from the current position.
    """

    # If Stockfish has no recommendation, we cannot compare.
    if not best_line:
        return None

    best_move = best_line[0]

    # The played move was the engine's preferred move.
    if move == best_move:
        return None

    # --------------------------------------------------
    # Missed capture
    # --------------------------------------------------

    if (
        board.is_capture(best_move)
        and not board.is_capture(move)
    ):

        try:
            captured_piece = board.piece_at(
                best_move.to_square
            )

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

    try:

        if (
            board.gives_check(best_move)
            and not board.gives_check(move)
        ):

            return (
                "You missed a stronger checking move that "
                "could have created a tactical opportunity."
            )

    except Exception:
        pass

    # --------------------------------------------------
    # Missed promotion
    # --------------------------------------------------

    try:

        moving_piece = board.piece_at(
            move.from_square
        )

        if moving_piece:

            if (
                moving_piece.piece_type == chess.PAWN
                and best_move.promotion is not None
                and chess.square_rank(
                    best_move.to_square
                ) in [0, 7]
            ):

                return (
                    "You missed an opportunity to "
                    "promote your pawn."
                )

    except Exception:
        pass

    return None

def detect_hanging_piece(board, move):
    """
    Detect whether the piece moved to a square where
    the opponent can immediately capture it.
    """

    temp_board = board.copy()

    try:
        temp_board.push(move)
    except Exception:
        return None

    # Find all opponent captures in the resulting position
    opponent_captures = []

    for opponent_move in temp_board.legal_moves:

        if temp_board.is_capture(opponent_move):
            opponent_captures.append(opponent_move)

    if not opponent_captures:
        return None

    # The piece that was just moved
    moved_piece = temp_board.piece_at(
        move.to_square
    )

    if moved_piece is None:
        return None

    piece_name = {
        chess.PAWN: "pawn",
        chess.KNIGHT: "knight",
        chess.BISHOP: "bishop",
        chess.ROOK: "rook",
        chess.QUEEN: "queen",
        chess.KING: "king"
    }.get(
        moved_piece.piece_type,
        "piece"
    )

    # Check whether the opponent can capture
    # the piece that was just moved.
    for capture in opponent_captures:

        if capture.to_square == move.to_square:

            return (
                f"Your {piece_name} can be captured "
                f"immediately by the opponent."
            )

    return None

def detect_fork(board, move):
    """
    Detect whether the move creates a fork,
    meaning the moved piece attacks two or more
    valuable enemy pieces.
    """

    temp_board = board.copy()

    try:
        temp_board.push(move)
    except Exception:
        return None

    moved_piece = temp_board.piece_at(
        move.to_square
    )

    if moved_piece is None:
        return None

    attacked_targets = []

    for square in chess.SQUARES:

        target = temp_board.piece_at(square)

        if target is None:
            continue

        # Only consider enemy pieces
        if target.color == moved_piece.color:
            continue

        # Don't count the king as a normal material target
        if target.piece_type == chess.KING:
            continue

        if temp_board.is_attacked_by(
            moved_piece.color,
            square
        ):
            attacked_targets.append(target)

    # We need at least two valuable targets
    valuable_targets = [
        piece for piece in attacked_targets
        if piece.piece_type in [
            chess.QUEEN,
            chess.ROOK,
            chess.BISHOP,
            chess.KNIGHT
        ]
    ]

    if len(valuable_targets) < 2:
        return None

    names = {
        chess.QUEEN: "queen",
        chess.ROOK: "rook",
        chess.BISHOP: "bishop",
        chess.KNIGHT: "knight"
    }

    target_names = [
        names[piece.piece_type]
        for piece in valuable_targets[:2]
    ]

    return (
        f"This move creates a fork, attacking the "
        f"opponent's {target_names[0]} and "
        f"{target_names[1]} at the same time."
    )

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
        reason, reason_type = generate_move_reason(
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
            "reason_type": reason_type,
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