import { useState } from "react";
import Upload from "./pages/Upload";
import PuzzleTrainer from "./pages/App";
import Analysis from "./pages/Analysis";
import MoveList from "./pages/MoveList";
import Report from "./pages/Report";

export default function App() {

  const [page, setPage] = useState("upload");

  return (
    <div>

      <div style={{ textAlign: "center", margin: "20px" }}>
        <button
          onClick={() => setPage("upload")}
          style={{ marginRight: "10px" }}
        >
          Upload Game
        </button>

        <button
          onClick={() => setPage("analysis")}
          style={{ marginRight: "10px" }}
        >
          Analysis Report
        </button>

        <button
          onClick={() => setPage("movelist")}
          style={{ marginRight: "10px" }}
        >
          Move List
        </button>

        <button
          onClick={() => setPage("puzzles")}
        >
          Puzzle Trainer
        </button>

        <button
          onClick={() => setPage("report")}
          style={{ marginRight: "10px" }}
        >
          Performance Report
        </button>
      </div>


      {page === "upload" && <Upload />}

      {page === "puzzles" && <PuzzleTrainer />}

      {page === "analysis" && <Analysis />}

      {page === "movelist" && <MoveList />}

      {page === "report" && <Report />}

    </div>
  );
}