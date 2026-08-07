import chess
import chess.engine

class ChessAnalysis: 

    def __init__ (self, stockfish_path):
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    def evaluate_position(self, board):
        info = self.engine.analyse(board, chess.engine.Limit(depth=15))
        score = info["score"].white().score(mate_score = 10000)
        return score

    def best_line(self, board, length=6):
        info = self.engine.analyse(
            board,
            chess.engine.Limit(depth=15)
        )

        return info["pv"][:length]

    def close(self):
        self.engine.quit()

    def classify_move(self, loss):
        if abs(loss) > 300:
            return "BLUNDER"
        elif abs(loss) > 100: 
            return "MISTAKE"
        elif abs(loss) > 50:
            return "INACCURACY"
        else:
            return "GOOD"

    def piece_value_loss(self, board_before, board_after):

        values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 0
        }

        before_material = 0
        after_material = 0

        for piece in board_before.piece_map().values():
            before_material += values[piece.piece_type]

        for piece in board_after.piece_map().values():
            after_material += values[piece.piece_type]

        return before_material - after_material