import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import { useEffect, useState } from "react";
import StatusMessage from "../components/StatusMessage";
import PuzzleInfo from "../components/PuzzleInfo";

export default function App() {
  const [game, setGame] = useState(null);
  const [message, setMessage] = useState("");
  const [solution, setSolution] = useState([]);
  const [currentMove, setCurrentMove] = useState(0);
  const [solved, setSolved] = useState(false);
  const [category, setCategory] = useState("");
  const [reason, setReason] = useState("");
  const [orientation, setOrientation] = useState("white");

  async function loadPuzzle() {
    const response = await fetch("http://127.0.0.1:5000/puzzles");
    const data = await response.json();

    console.log("Puzzles received:", data);

    const puzzles = data.puzzles;

    const randomPuzzle =
      puzzles[Math.floor(Math.random() * puzzles.length)];

    console.log("Selected puzzle:", randomPuzzle);

    const newGame = new Chess(randomPuzzle.fen);

    setGame(newGame);

    const turn = randomPuzzle.fen.split(" ")[1];

    setOrientation(turn === "w" ? "white" : "black");
    console.log("Turn:", turn);
    console.log("Orientation:", turn === "w" ? "white" : "black");
    setSolution(randomPuzzle.solution);
    setCategory(randomPuzzle.category);
    setReason(randomPuzzle.reason);
    setMessage("");
    setSolved(false);
    setCurrentMove(0);
  }

  useEffect(() => {
    loadPuzzle();
  }, []);

  function playOpponentMove(move, currentPosition) {

    console.log("Opponent is playing:", move);
    const gameCopy = new Chess(currentPosition.fen());

    gameCopy.move({
      from: move.substring(0, 2),
      to: move.substring(2, 4),
      promotion: "q",
    });

    setGame(gameCopy);
  }

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


    const playedMove = sourceSquare + targetSquare;

    console.log("Played:", playedMove);
    console.log("Expected:", solution[currentMove]);


    // Wrong move
    if (playedMove !== solution[currentMove]) {

      setMessage("❌ Incorrect. Try again.");
      return false;

    }


    // Correct player move
    setGame(gameCopy);


    let nextMoveIndex = currentMove + 1;


    // Puzzle finished
    if (nextMoveIndex >= solution.length) {

      setMessage("🎉 Puzzle solved!");
      setSolved(true);
      return true;

    }


    // Let opponent respond
    setMessage("✅ Correct!");


    setTimeout(() => {

      const opponentMove = solution[nextMoveIndex];

      playOpponentMove(opponentMove, gameCopy);


      nextMoveIndex++;

      // Move counter skips opponent move
      setCurrentMove(nextMoveIndex);


      if (nextMoveIndex >= solution.length) {
        setMessage("🎉 Puzzle solved!");
        setSolved(true);
      }


    }, 700);


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
          boardOrientation: orientation,
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