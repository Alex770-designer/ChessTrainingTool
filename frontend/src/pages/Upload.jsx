import { useState } from "react";

export default function Upload() {
  const [pgn, setPgn] = useState("");
  const [message, setMessage] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);

  const [chessUsername, setChessUsername] = useState("");
  const [chessDate, setChessDate] = useState("");
  const [chessGameUrl, setChessGameUrl] = useState("");

  const [lichessGameUrl, setLichessGameUrl] = useState("");

  function handleFileChange(event) {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    if (!file.name.toLowerCase().endsWith(".pgn")) {
      setMessage("❌ Please select a .pgn file.");
      return;
    }

    setSelectedFile(file);

    const reader = new FileReader();

    reader.onload = (event) => {
      setPgn(event.target.result);
      setMessage(`Loaded ${file.name}`);
    };

    reader.onerror = () => {
      setMessage("❌ Could not read the file.");
    };

    reader.readAsText(file);
  }

  async function submitPGN() {
    if (!pgn.trim()) {
      setMessage(
        "❌ Please paste a PGN or upload a .pgn file."
      );
      return;
    }

    setMessage("⏳ Analyzing game...");

    try {
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

      if (!response.ok) {
        setMessage(
          `❌ ${data.message || "Error analyzing game."}`
        );
        return;
      }

      setMessage(
        `✅ ${data.message} Moves analyzed: ${data.moves_analyzed}, Puzzles created: ${data.puzzles_created}`
      );
    } catch (error) {
      console.error(error);

      setMessage(
        "❌ Could not connect to the analysis server."
      );
    }
  }

  async function importChessComGame() {
    if (
      !chessUsername.trim() ||
      !chessDate ||
      !chessGameUrl.trim()
    ) {
      setMessage(
        "❌ Please enter your username, game date, and game URL."
      );
      return;
    }

    setMessage(
      "⏳ Importing and analyzing Chess.com game..."
    );

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/import-chess-com",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: chessUsername,
            date: chessDate,
            game_url: chessGameUrl,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(
          `❌ ${data.message || "Error importing Chess.com game."}`
        );
        return;
      }

      setMessage(
        `✅ ${data.message} Moves analyzed: ${data.moves_analyzed}, Puzzles created: ${data.puzzles_created}`
      );
    } catch (error) {
      console.error(error);

      setMessage(
        "❌ Could not connect to the analysis server."
      );
    }
  }

  async function importLichessGame() {
    if (!lichessGameUrl.trim()) {
      setMessage("❌ Please enter a Lichess game URL.");
      return;
    }

    setMessage("⏳ Importing and analyzing Lichess game...");

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/import-lichess",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            game_url: lichessGameUrl,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(
          `❌ ${data.message || "Error importing Lichess game."}`
        );
        return;
      }

      setMessage(
        `✅ ${data.message} Moves analyzed: ${data.moves_analyzed}, Puzzles created: ${data.puzzles_created}`
      );
    } catch (error) {
      console.error(error);

      setMessage(
        "❌ Could not connect to the analysis server."
      );
    }
  }

  return (
    <div
      style={{
        width: "700px",
        margin: "40px auto",
        textAlign: "center",
      }}
    >
      <h1>Upload Chess Game</h1>

      <h3>Paste PGN</h3>

      <textarea
        value={pgn}
        onChange={(e) => {
          setPgn(e.target.value);
          setSelectedFile(null);
        }}
        placeholder="Paste PGN here..."
        style={{
          width: "100%",
          height: "250px",
          fontSize: "16px",
        }}
      />

      <button
        onClick={submitPGN}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          fontSize: "18px",
          cursor: "pointer",
        }}
      >
        Analyze Game
      </button>

      <h3
        style={{
          marginTop: "40px",
        }}
      >
        Or upload a PGN file
      </h3>

      <input
        type="file"
        accept=".pgn"
        onChange={handleFileChange}
      />

      {selectedFile && (
        <p>
          📄 Selected: {selectedFile.name}
        </p>
      )}

      <h2
        style={{
          marginTop: "50px",
        }}
      >
        Chess.com Import
      </h2>

      <p>
        Import a game directly from Chess.com.
      </p>

      <div
        style={{
          textAlign: "left",
          marginTop: "20px",
        }}
      >
        <label>
          <strong>Chess.com Username</strong>
        </label>

        <input
          type="text"
          value={chessUsername}
          onChange={(e) =>
            setChessUsername(e.target.value)
          }
          placeholder="e.g. s137340"
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            fontSize: "16px",
            boxSizing: "border-box",
          }}
        />

        <label
          style={{
            display: "block",
            marginTop: "20px",
          }}
        >
          <strong>Game Date</strong>
        </label>

        <input
          type="date"
          value={chessDate}
          onChange={(e) =>
            setChessDate(e.target.value)
          }
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            fontSize: "16px",
            boxSizing: "border-box",
          }}
        />

        <label
          style={{
            display: "block",
            marginTop: "20px",
          }}
        >
          <strong>Game URL</strong>
        </label>

        <input
          type="text"
          value={chessGameUrl}
          onChange={(e) =>
            setChessGameUrl(e.target.value)
          }
          placeholder="https://www.chess.com/game/live/..."
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            fontSize: "16px",
            boxSizing: "border-box",
          }}
        />
      </div>

      <h2 style={{ marginTop: "50px" }}>
        Lichess Import
      </h2>

      <p>
        Import a game directly from Lichess.
      </p>

      <div
        style={{
          textAlign: "left",
          marginTop: "20px",
        }}
      >
        <label>
          <strong>Game URL</strong>
        </label>

        <input
          type="text"
          value={lichessGameUrl}
          onChange={(e) =>
            setLichessGameUrl(e.target.value)
          }
          placeholder="https://lichess.org/..."
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            fontSize: "16px",
            boxSizing: "border-box",
          }}
        />
      </div>

      <button
        onClick={importLichessGame}
        style={{
          marginTop: "25px",
          padding: "10px 20px",
          fontSize: "18px",
          cursor: "pointer",
        }}
      >
        Import Lichess Game
      </button>

      <button
        onClick={importChessComGame}
        style={{
          marginTop: "25px",
          padding: "10px 20px",
          fontSize: "18px",
          cursor: "pointer",
        }}
      >
        Import Chess.com Game
      </button>

      <p>{message}</p>
    </div>
  );
}