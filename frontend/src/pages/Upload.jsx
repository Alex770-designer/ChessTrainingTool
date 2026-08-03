import { useState } from "react";

export default function Upload() {

  const [pgn, setPgn] = useState("");
  const [message, setMessage] = useState("");

  async function submitPGN() {

    const response = await fetch(
      "http://127.0.0.1:5000/upload",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          pgn: pgn,
        }),
      }
    );

    const data = await response.json();

    setMessage(
  `${data.message} Moves analyzed: ${data.moves_analyzed}, Puzzles created: ${data.puzzles_created}`
    );
  }


  return (
    <div
      style={{
        width: "700px",
        margin: "40px auto",
        textAlign: "center",
      }}
    >

      <h1>
        Upload Chess Game
      </h1>

      <textarea
        value={pgn}
        onChange={(e) => setPgn(e.target.value)}
        placeholder="Paste PGN here..."
        style={{
          width: "100%",
          height: "250px",
          fontSize: "16px",
        }}
      />

      <br />

      <button
        onClick={submitPGN}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          fontSize: "18px",
        }}
      >
        Analyze Game
      </button>

      <p>
        {message}
      </p>

    </div>
  );
}