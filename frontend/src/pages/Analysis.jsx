import { useEffect, useState } from "react";

export default function Analysis() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/analysis")
      .then((response) => response.json())
      .then((data) => {
        console.log("Analysis report received:", data);

        if (data.error) {
          setError(data.error);
          return;
        }

        setReport(data);
      })
      .catch((err) => {
        console.error(err);
        setError("Could not load the analysis report.");
      });
  }, []);

  if (error) {
    return (
      <div
        style={{
          width: "800px",
          margin: "40px auto",
          textAlign: "center",
        }}
      >
        <h1>Game Analysis</h1>
        <p>❌ {error}</p>
      </div>
    );
  }

  if (!report) {
    return (
      <div
        style={{
          width: "800px",
          margin: "40px auto",
          textAlign: "center",
        }}
      >
        <h1>Game Analysis</h1>
        <p>⏳ Loading analysis...</p>
      </div>
    );
  }

  const { phases, overall } = report;

  return (
    <div
      style={{
        width: "900px",
        maxWidth: "90%",
        margin: "40px auto",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1 style={{ textAlign: "center" }}>
        Chess Analysis Report
      </h1>

      {/* ============================== */}
      {/* OVERALL PERFORMANCE */}
      {/* ============================== */}

      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "10px",
          padding: "25px",
          marginTop: "30px",
        }}
      >
        <h2>Overall Performance</h2>

        <p>
          <strong>Strongest Phase:</strong>{" "}
          {overall.best_phase || "N/A"}
        </p>

        <p>
          <strong>Weakest Phase:</strong>{" "}
          {overall.worst_phase || "N/A"}
        </p>

        <hr />

        <h3>Summary</h3>
        <p>{overall.summary || "N/A"}</p>

        <h3>Strength</h3>
        <p>{overall.strength || "N/A"}</p>

        <h3>Weakness</h3>
        <p>{overall.weakness || "N/A"}</p>

        <h3>Recommended Focus</h3>
        <p>{overall.focus || "N/A"}</p>
      </div>

      {/* ============================== */}
      {/* PHASE BREAKDOWN */}
      {/* ============================== */}

      <h2
        style={{
          marginTop: "40px",
          textAlign: "center",
        }}
      >
        Phase Breakdown
      </h2>

      {Object.entries(phases).map(
        ([phase, data]) => (
          <div
            key={phase}
            style={{
              border: "1px solid #ccc",
              borderRadius: "10px",
              padding: "25px",
              marginTop: "20px",
            }}
          >
            <h2>{phase}</h2>

            <p>
              <strong>Summary:</strong>{" "}
              {data.summary}
            </p>

            {/* ============================== */}
            {/* YOU */}
            {/* ============================== */}

            <div
              style={{
                marginTop: "20px",
                padding: "15px",
                backgroundColor: "#f5f5f5",
                borderRadius: "8px",
              }}
            >
              <h3>You</h3>

              <p>
                <strong>Performance:</strong>{" "}
                {data.you.performance}
              </p>

              <p>
                <strong>Moves:</strong>{" "}
                {data.you.moves}
              </p>

              <p>
                <strong>Blunders:</strong>{" "}
                {data.you.blunders}
              </p>

              <p>
                <strong>Mistakes:</strong>{" "}
                {data.you.mistakes}
              </p>

              <p>
                <strong>Inaccuracies:</strong>{" "}
                {data.you.inaccuracies}
              </p>

              <p>
                <strong>Average Loss:</strong>{" "}
                {data.you.average_loss}
              </p>

              <p>
                <strong>Largest Loss:</strong>{" "}
                {data.you.largest_loss}
              </p>
            </div>

            {/* ============================== */}
            {/* OPPONENT */}
            {/* ============================== */}

            <div
              style={{
                marginTop: "15px",
                padding: "15px",
                backgroundColor: "#f5f5f5",
                borderRadius: "8px",
              }}
            >
              <h3>Opponent</h3>

              <p>
                <strong>Performance:</strong>{" "}
                {data.opponent.performance}
              </p>

              <p>
                <strong>Moves:</strong>{" "}
                {data.opponent.moves}
              </p>

              <p>
                <strong>Blunders:</strong>{" "}
                {data.opponent.blunders}
              </p>

              <p>
                <strong>Mistakes:</strong>{" "}
                {data.opponent.mistakes}
              </p>

              <p>
                <strong>Inaccuracies:</strong>{" "}
                {data.opponent.inaccuracies}
              </p>

              <p>
                <strong>Average Loss:</strong>{" "}
                {data.opponent.average_loss}
              </p>

              <p>
                <strong>Largest Loss:</strong>{" "}
                {data.opponent.largest_loss}
              </p>
            </div>

            {/* ============================== */}
            {/* YOUR RECURRING PATTERNS */}
            {/* ============================== */}

            <div style={{ marginTop: "20px" }}>
              <h3>Your Recurring Patterns</h3>

              {data.you.patterns &&
              data.you.patterns.length > 0 ? (
                <ul>
                  {data.you.patterns.map(
                    (pattern, index) => (
                      <li key={index}>
                        <strong>
                          {pattern.type ||
                            pattern.reason}
                        </strong>

                        {" × "}
                        {pattern.count}

                        {pattern.description && (
                          <>
                            {" - "}
                            {pattern.description}
                          </>
                        )}
                      </li>
                    )
                  )}
                </ul>
              ) : (
                <p>
                  No significant recurring patterns
                  detected.
                </p>
              )}
            </div>

            {/* ============================== */}
            {/* OPPONENT PATTERNS */}
            {/* ============================== */}

            <div style={{ marginTop: "20px" }}>
              <h3>Opponent Recurring Patterns</h3>

              {data.opponent.patterns &&
              data.opponent.patterns.length > 0 ? (
                <ul>
                  {data.opponent.patterns.map(
                    (pattern, index) => (
                      <li key={index}>
                        <strong>
                          {pattern.type ||
                            pattern.reason}
                        </strong>

                        {" × "}
                        {pattern.count}

                        {pattern.description && (
                          <>
                            {" - "}
                            {pattern.description}
                          </>
                        )}
                      </li>
                    )
                  )}
                </ul>
              ) : (
                <p>
                  No significant recurring patterns
                  detected.
                </p>
              )}
            </div>
          </div>
        )
      )}
    </div>
  );
}