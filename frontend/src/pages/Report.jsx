import { useEffect, useState } from "react";

export default function Report() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/report")
      .then((response) => response.json())
      .then((data) => {
        console.log("Report received:", data);
        setReport(data);
      })
      .catch((error) => {
        console.error(error);
        setError("Could not load report.");
      });
  }, []);

  if (error) {
    return <h2 style={{ textAlign: "center" }}>{error}</h2>;
  }

  if (!report) {
    return (
      <h2 style={{ textAlign: "center", marginTop: "40px" }}>
        Loading report...
      </h2>
    );
  }

  const phases = report.phases;
  const overall = report.overall;

  return (
    <div
      style={{
        width: "900px",
        margin: "40px auto",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1 style={{ textAlign: "center" }}>
        Chess Performance Report
      </h1>

      {/* Overall */}
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "10px",
          padding: "25px",
          marginTop: "30px",
        }}
      >
        <h2>Overall Performance</h2>

        <p>{overall.summary}</p>

        <h3>💪 Biggest Strength</h3>
        <p>{overall.strength}</p>

        <h3>⚠️ Biggest Weakness</h3>
        <p>{overall.weakness}</p>

        <h3>🎯 Recommended Focus</h3>
        <p>{overall.focus}</p>
      </div>

      {/* Phase Reports */}

      {Object.entries(phases).map(([phase, data]) => (
        <div
          key={phase}
          style={{
            border: "1px solid #ccc",
            borderRadius: "10px",
            padding: "25px",
            marginTop: "25px",
          }}
        >
          <h2>{phase}</h2>

          <p>{data.summary}</p>

          <h3>
            Your Performance: {data.you.performance}
          </h3>

          {data.you.moves > 0 ? (
            <>
              <p>
                Moves: {data.you.moves}
              </p>

              <p>
                🔴 Blunders: {data.you.blunders}
              </p>

              <p>
                🟠 Mistakes: {data.you.mistakes}
              </p>

              <p>
                🟡 Inaccuracies: {data.you.inaccuracies}
              </p>

              <p>
                Average evaluation loss:{" "}
                {data.you.average_loss}
              </p>
            </>
          ) : (
            <p>No moves played in this phase.</p>
          )}

          <h3>
            Opponent Performance:{" "}
            {data.opponent.performance}
          </h3>

          {data.opponent.moves > 0 ? (
            <>
              <p>
                Moves: {data.opponent.moves}
              </p>

              <p>
                🔴 Blunders: {data.opponent.blunders}
              </p>

              <p>
                🟠 Mistakes: {data.opponent.mistakes}
              </p>

              <p>
                🟡 Inaccuracies: {data.opponent.inaccuracies}
              </p>

              <p>
                Average evaluation loss:{" "}
                {data.opponent.average_loss}
              </p>
            </>
          ) : (
            <p>No moves played in this phase.</p>
          )}

          {/* Patterns */}

          {data.you.patterns.length > 0 && (
            <>
              <h3>Your Main Mistake Patterns</h3>

              <ul>
                {data.you.patterns.map(
                  (pattern, index) => (
                    <li key={index}>
                      {pattern.reason}{" "}
                      <strong>
                        ({pattern.count})
                      </strong>
                    </li>
                  )
                )}
              </ul>
            </>
          )}
        </div>
      ))}
    </div>
  );
}