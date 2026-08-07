import { useEffect, useState } from "react";

export default function Analysis() {

  const [analysis, setAnalysis] = useState([]);

  useEffect(() => {

    fetch("http://127.0.0.1:5000/analysis")
      .then(response => response.json())
      .then(data => {
        console.log("Analysis received:", data);
        setAnalysis(data);
      });

  }, []);


  const whiteMoves = analysis.filter(
    move => move.fen.split(" ")[1] === "w"
    );

    const blackMoves = analysis.filter(
    move => move.fen.split(" ")[1] === "b"
    );


    const countCategory = (moves, category) =>
    moves.filter(
        move => move.category === category
    ).length;


    const whiteBlunders = countCategory(
    whiteMoves,
    "BLUNDER"
    );

    const blackBlunders = countCategory(
    blackMoves,
    "BLUNDER"
    );


    const whiteMistakes = countCategory(
    whiteMoves,
    "MISTAKE"
    );

    const blackMistakes = countCategory(
    blackMoves,
    "MISTAKE"
    );


    const whiteInaccuracies = countCategory(
    whiteMoves,
    "INACCURACY"
    );

    const blackInaccuracies = countCategory(
    blackMoves,
    "INACCURACY"
    );

  return (
    <div
      style={{
        width: "800px",
        margin: "40px auto",
        textAlign: "center"
      }}
    >

      <h1>Game Analysis</h1>


      <h2>
        Moves analyzed: {analysis.length}
      </h2>


      <div>
        <h3>Summary</h3>


            <h4>White</h4>

            <p>
            🔴 Blunders: {whiteBlunders}
            </p>

            <p>
            🟠 Mistakes: {whiteMistakes}
            </p>

            <p>
            🟡 Inaccuracies: {whiteInaccuracies}
            </p>



            <h4>Black</h4>

            <p>
            🔴 Blunders: {blackBlunders}
            </p>

            <p>
            🟠 Mistakes: {blackMistakes}
            </p>

            <p>
            🟡 Inaccuracies: {blackInaccuracies}
            </p>

      </div>


      <h2>Critical Moments</h2>


      {analysis.map((move, index) => (

        move.category !== "GOOD" && (

          <div
            key={index}
            style={{
              border:"1px solid black",
              margin:"10px",
              padding:"10px"
            }}
          >

            <h3>
              Move {move.move_number}
            </h3>


            <p>
              Played: {move.move}
            </p>


            <p>
              Best line:
              {
                move.best_line
                  ? move.best_line.join(" ")
                  : move.best_move
              }
            </p>


            <p>
              Category:
              {move.category}
            </p>


            <p>
              Reason:
              {move.reason}
            </p>


          </div>

        )

      ))}


    </div>
  );
}