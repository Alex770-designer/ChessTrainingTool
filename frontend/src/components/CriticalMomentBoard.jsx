import { useEffect, useState } from "react";
import { Chess } from "chess.js";

const pieceSymbols = {
  p: "♟",
  r: "♜",
  n: "♞",
  b: "♝",
  q: "♛",
  k: "♚",
  P: "♙",
  R: "♖",
  N: "♘",
  B: "♗",
  Q: "♕",
  K: "♔",
};

function parseFEN(fen) {
  const boardPart = fen.split(" ")[0];
  const rows = boardPart.split("/");

  const board = [];

  for (const row of rows) {
    const currentRow = [];

    for (const character of row) {
      if (!isNaN(character)) {
        const emptySquares = Number(character);

        for (let i = 0; i < emptySquares; i++) {
          currentRow.push(null);
        }
      } else {
        currentRow.push(character);
      }
    }

    board.push(currentRow);
  }

  return board;
}

function squareName(row, column, playerColor) {
  const files =
    playerColor === "black"
      ? ["h", "g", "f", "e", "d", "c", "b", "a"]
      : ["a", "b", "c", "d", "e", "f", "g", "h"];

  const ranks =
    playerColor === "black"
      ? ["1", "2", "3", "4", "5", "6", "7", "8"]
      : ["8", "7", "6", "5", "4", "3", "2", "1"];

  return `${files[column]}${ranks[row]}`;
}

function boardFromChess(chess, playerColor) {
  const fen = chess.fen();
  let board = parseFEN(fen);

  if (playerColor === "black") {
    board = [...board]
      .reverse()
      .map((row) => [...row].reverse());
  }

  return board;
}

export default function CriticalMomentBoard({
  fen,
  playerColor = "white",
  onMove,
  resetKey = 0,
  showBestMove = false,
  bestMove = null,
}) {
  const [chess, setChess] = useState(() => new Chess(fen));
  const [selectedSquare, setSelectedSquare] = useState(null);
  const [message, setMessage] = useState("");
  const [attempted, setAttempted] = useState(false);
  const [board, setBoard] = useState(() =>
    boardFromChess(new Chess(fen), playerColor)
  );

  useEffect(() => {
    const newChess = new Chess(fen);

    setChess(newChess);
    setBoard(boardFromChess(newChess, playerColor));
    setSelectedSquare(null);
    setMessage("");
    setAttempted(false);
  }, [fen, resetKey, playerColor]);

  useEffect(() => {
    if (!showBestMove || !bestMove) {
      return;
    }

    const from = bestMove.substring(0, 2);
    const to = bestMove.substring(2, 4);

    const newChess = new Chess(fen);

    try {
      const move = newChess.move({
        from,
        to,
        promotion: "q",
      });

      if (!move) {
        return;
      }

      setChess(newChess);
      setBoard(boardFromChess(newChess, playerColor));
      setSelectedSquare(null);
      setMessage(`Best move: ${move.san}`);
    } catch (error) {
      console.error("Could not show best move:", error);
    }
  }, [showBestMove, bestMove, fen, playerColor]);

  const sideToMove =
    chess.turn() === "b" ? "Black" : "White";

  const files =
    playerColor === "black"
      ? ["h", "g", "f", "e", "d", "c", "b", "a"]
      : ["a", "b", "c", "d", "e", "f", "g", "h"];

  const ranks =
    playerColor === "black"
      ? ["1", "2", "3", "4", "5", "6", "7", "8"]
      : ["8", "7", "6", "5", "4", "3", "2", "1"];

  function handleSquareClick(square) {
    setMessage("");

    if (showBestMove || attempted) {
        setMessage("This attempt is complete. Try again to reset the position.");
        return;
    }

    if (!selectedSquare) {
      setMessage("Reset the position before trying again.");
      return;
    }

    if (!selectedSquare) {
      const piece = chess.get(square);

      if (!piece) {
        setMessage("Select one of your pieces.");
        return;
      }

      const expectedColor =
        sideToMove === "White" ? "w" : "b";

      if (piece.color !== expectedColor) {
        setMessage("That piece cannot move right now.");
        return;
      }

      if (
        (playerColor === "white" && piece.color !== "w") ||
        (playerColor === "black" && piece.color !== "b")
      ) {
        setMessage("Select one of your pieces.");
        return;
      }

      setSelectedSquare(square);
      return;
    }

    if (selectedSquare === square) {
      setSelectedSquare(null);
      return;
    }

    try {
      const move = chess.move({
        from: selectedSquare,
        to: square,
        promotion: "q",
      });

      if (!move) {
        setMessage("That is not a legal move.");
        return;
      }

      const userMove = {
        from: selectedSquare,
        to: square,
        san: move.san,
        uci: `${selectedSquare}${square}`,
      };

      setBoard(boardFromChess(chess, playerColor));
      setSelectedSquare(null);
      setAttempted(true);
      setMessage(`You played ${move.san}`);

      if (onMove) {
        onMove(userMove);
      }
    } catch (error) {
      setMessage("That is not a legal move.");
    }
  }

  return (
    <div
      style={{
        width: "360px",
        maxWidth: "100%",
        margin: "20px auto",
        textAlign: "center",
      }}
    >
      <div
        style={{
          marginBottom: "10px",
          fontSize: "14px",
        }}
      >
        <strong>{sideToMove} to move</strong>
        {" • "}
        You are playing{" "}
        {playerColor === "black" ? "Black" : "White"}
      </div>

      {selectedSquare && !showBestMove && (
        <div
          style={{
            marginBottom: "10px",
            fontSize: "14px",
          }}
        >
          Selected: <strong>{selectedSquare}</strong>
          <br />
          Click a destination square.
        </div>
      )}

      {message && (
        <div
          style={{
            marginBottom: "10px",
            padding: "8px",
            borderRadius: "6px",
            backgroundColor: "#f5f5f5",
            fontSize: "14px",
          }}
        >
          {message}
        </div>
      )}

      <div
        style={{
          border: "3px solid #333",
          width: "100%",
        }}
      >
        {board.map((row, rowIndex) =>
          row.map((piece, columnIndex) => {
            const isLightSquare =
              (rowIndex + columnIndex) % 2 === 0;

            const square = squareName(
              rowIndex,
              columnIndex,
              playerColor
            );

            const isSelected =
              selectedSquare === square;

            const showFileLabel = rowIndex === 7;
            const showRankLabel = columnIndex === 0;

            return (
              <button
                key={`${rowIndex}-${columnIndex}`}
                onClick={() => handleSquareClick(square)}
                style={{
                  width: "12.5%",
                  aspectRatio: "1",
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  verticalAlign: "top",
                  position: "relative",
                  backgroundColor: isSelected
                    ? "#f6f669"
                    : isLightSquare
                    ? "#f0d9b5"
                    : "#b58863",
                  border: "none",
                  padding: 0,
                  margin: 0,
                  fontSize: "36px",
                  lineHeight: "1",
                  cursor: showBestMove
                    ? "default"
                    : "pointer",
                  userSelect: "none",
                }}
              >
                {piece ? pieceSymbols[piece] : ""}

                {showFileLabel && (
                  <span
                    style={{
                      position: "absolute",
                      bottom: "2px",
                      right: "3px",
                      fontSize: "10px",
                      fontWeight: "bold",
                      color: isLightSquare
                        ? "#b58863"
                        : "#f0d9b5",
                      pointerEvents: "none",
                    }}
                  >
                    {files[columnIndex]}
                  </span>
                )}

                {showRankLabel && (
                  <span
                    style={{
                      position: "absolute",
                      top: "2px",
                      left: "3px",
                      fontSize: "10px",
                      fontWeight: "bold",
                      color: isLightSquare
                        ? "#b58863"
                        : "#f0d9b5",
                      pointerEvents: "none",
                    }}
                  >
                    {ranks[rowIndex]}
                  </span>
                )}
              </button>
            );
          })
        )}
      </div>
    </div>
  );
}