import chess


def count_pieces(board):
    """
    Count the remaining pieces on the board.
    """

    return {
        "queens": len(board.pieces(chess.QUEEN, chess.WHITE))
        + len(board.pieces(chess.QUEEN, chess.BLACK)),

        "rooks": len(board.pieces(chess.ROOK, chess.WHITE))
        + len(board.pieces(chess.ROOK, chess.BLACK)),

        "bishops": len(board.pieces(chess.BISHOP, chess.WHITE))
        + len(board.pieces(chess.BISHOP, chess.BLACK)),

        "knights": len(board.pieces(chess.KNIGHT, chess.WHITE))
        + len(board.pieces(chess.KNIGHT, chess.BLACK)),
    }


def development_score(board):
    """
    Estimate how developed the position is.

    Points are awarded when knights and bishops
    leave their original squares and when kings castle.
    """

    score = 0

    # White knights
    if chess.KNIGHT not in board.piece_map().values():
        pass

    if board.piece_at(chess.B1) != chess.Piece(
        chess.KNIGHT, chess.WHITE
    ):
        score += 1

    if board.piece_at(chess.G1) != chess.Piece(
        chess.KNIGHT, chess.WHITE
    ):
        score += 1

    # Black knights
    if board.piece_at(chess.B8) != chess.Piece(
        chess.KNIGHT, chess.BLACK
    ):
        score += 1

    if board.piece_at(chess.G8) != chess.Piece(
        chess.KNIGHT, chess.BLACK
    ):
        score += 1

    # White bishops
    if board.piece_at(chess.C1) != chess.Piece(
        chess.BISHOP, chess.WHITE
    ):
        score += 1

    if board.piece_at(chess.F1) != chess.Piece(
        chess.BISHOP, chess.WHITE
    ):
        score += 1

    # Black bishops
    if board.piece_at(chess.C8) != chess.Piece(
        chess.BISHOP, chess.BLACK
    ):
        score += 1

    if board.piece_at(chess.F8) != chess.Piece(
        chess.BISHOP, chess.BLACK
    ):
        score += 1

    # Castling is a strong sign that the opening
    # is progressing.
    if board.has_castling_rights(chess.WHITE) is False:
        score += 1

    if board.has_castling_rights(chess.BLACK) is False:
        score += 1

    return score


def classify_position(fen):

    board = chess.Board(fen)

    pieces = count_pieces(board)

    queens = pieces["queens"]
    rooks = pieces["rooks"]
    bishops = pieces["bishops"]
    knights = pieces["knights"]

    minor_pieces = bishops + knights
    total_non_pawn_pieces = (
        queens +
        rooks +
        bishops +
        knights
    )

    development = development_score(board)

    # --------------------------------------------------
    # ENDGAME
    # --------------------------------------------------

    if queens == 0:

        if total_non_pawn_pieces <= 4:
            return "ENDGAME"

        if rooks == 0 and minor_pieces <= 3:
            return "ENDGAME"

    # --------------------------------------------------
    # OPENING
    # --------------------------------------------------

    if board.fullmove_number <= 12:

        if development < 7:
            return "OPENING"

    # --------------------------------------------------
    # MIDDLEGAME
    # --------------------------------------------------

    return "MIDDLEGAME"


def classify_analysis(analysis):

    for move in analysis:

        move["phase"] = classify_position(
            move["fen"]
        )

    return analysis


if __name__ == "__main__":

    test_positions = [

        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "Starting position"
        ),

        (
            "r1bq1rk1/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQ1RK1 w - - 0 8",
            "Developed position"
        ),

        (
            "8/5pk1/6p1/7p/8/5P2/5KP1/8 w - - 0 40",
            "King and pawn endgame"
        )
    ]

    for fen, name in test_positions:

        print(
            f"{name}: "
            f"{classify_position(fen)}"
        )