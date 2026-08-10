import { useEffect, useState } from "react";

export default function MoveList() {
  const [analysis, setAnalysis] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/analysis")
      .then((response) => response.json())
      .then((data) => {
        console.log("Analysis received:", data);
        setAnalysis(data.analysis);
      });
  }, []);

  return (
    <div
      style={{
        width: "800px",
        margin: "40px auto",
        textAlign: "center",
      }}
    >
      <h1>Move List</h1>

      <p>
        Moves analyzed: {analysis.length}
      </p>

      <div
        style={{
          border: "1px solid black",
          padding: "15px",
          marginTop: "20px",
          textAlign: "left",
        }}
      >
        {analysis.map((move, index) => {
          const isWhite =
            move.fen.split(" ")[1] === "w";

          if (!isWhite) {
            return null;
          }

          const nextMove = analysis[index + 1];

          return (
            <div
              key={index}
              style={{
                display: "flex",
                alignItems: "center",
                padding: "8px 0",
                borderBottom: "1px solid #ddd",
              }}
            >
              <strong
                style={{
                  width: "60px",
                }}
              >
                {move.move_number}.
              </strong>

              <span
                style={{
                  width: "150px",
                }}
              >
                {move.move}

                {move.category !== "GOOD" && (
                  <span>
                    {" "}
                    {move.category === "BLUNDER"
                      ? "🔴"
                      : move.category === "MISTAKE"
                      ? "🟠"
                      : "🟡"}
                  </span>
                )}
              </span>

              <span
                style={{
                  width: "150px",
                }}
              >
                {nextMove &&
                nextMove.fen.split(" ")[1] === "b"
                  ? nextMove.move
                  : ""}

                {nextMove &&
                  nextMove.category !== "GOOD" && (
                    <span>
                      {" "}
                      {nextMove.category === "BLUNDER"
                        ? "🔴"
                        : nextMove.category === "MISTAKE"
                        ? "🟠"
                        : "🟡"}
                    </span>
                  )}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}