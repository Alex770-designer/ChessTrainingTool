import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import { useEffect, useState } from "react";
import StatusMessage from "../components/StatusMessage";
import PuzzleInfo from "../components/PuzzleInfo";

export default function App() {
  const [game, setGame] = useState(null);
  const [message, setMessage] = useState("");
  const [solution, setSolution] = useState("");
  const [solved, setSolved] = useState(false);
  const [category, setCategory] = useState("");
  const [reason, setReason] = useState("");

  async function loadPuzzle() {
    const response = await fetch("http://127.0.0.1:5000/puzzles");
    const data = await response.json();

    console.log("Puzzles received:", data);

    const puzzles = data.puzzles;

    const randomPuzzle =
      puzzles[Math.floor(Math.random() * puzzles.length)];

    console.log("Selected puzzle:", randomPuzzle);

    setGame(new Chess(randomPuzzle.fen));
    setSolution(randomPuzzle.solution);
    setCategory(randomPuzzle.category);
    setReason(randomPuzzle.reason);
    setMessage("");
    setSolved(false);
  }

  useEffect(() => {
    loadPuzzle();
  }, []);

  function onDrop({ sourceSquare, targetSquare }) {
    const gameCopy = new Chess(game.fen());

    const moveResult = gameCopy.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: "q",
    });

    if (!moveResult) {
      return false;
    }

    console.log("Played move:", sourceSquare + targetSquare);
    console.log("Solution:", solution);

    if (sourceSquare + targetSquare === solution) {
      setMessage("✅ Correct! Great find.");
      setSolved(true);
    } else {
      setMessage("❌ Incorrect. Try again.");
      return false;
    }

    setGame(gameCopy);

    return true;
  }

  return (
    <div
      style={{
        width: "600px",
        margin: "40px auto",
        textAlign: "center",
      }}
    >
      <h1>Chess Training Tool</h1>

      <Chessboard
        options={{
          position: game ? game.fen() : undefined,
          onPieceDrop: onDrop,
        }}
      />

      <StatusMessage message={message} />
      <PuzzleInfo 
        category={category}
        reason={reason}
      />

      {solved && (
        <button
          onClick={loadPuzzle}
          style={{
            marginTop: "20px",
            padding: "10px 20px",
            fontSize: "18px",
            cursor: "pointer",
          }}
        >
          Next Puzzle
        </button>
      )}
    </div>
  );
}