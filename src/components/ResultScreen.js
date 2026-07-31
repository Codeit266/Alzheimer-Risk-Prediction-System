import Visualization from "./Visualization";

function ResultScreen({ result, answers }) {

  if (!result) {
    return <p className="screenText">Processing results...</p>;
  }

  const getPredictionClass = (pred) => {
    if (!pred) return "";
    const lower = pred.toLowerCase();
    if (lower.includes("no risk")) return "norisk";
    if (lower.includes("insufficient") || lower.includes("uncertain") || lower.includes("unknown")) return "uncertain";
    if (lower.includes("risk")) return "risk";
    return "";
  };

  const predClass = getPredictionClass(result.prediction);

  return (
    <div className="screen resultsWide">

      <h2 className="screenTitle" style={{ marginBottom: "16px" }}>
        Screening Result
      </h2>

      <div className="resultsTopGrid">
        <div className="predictionCard">
          <div className="predictionTitle">
            Prediction: <span className={`predictionValue ${predClass}`}>{result.prediction}</span>
          </div>
          <div className="confidenceText">
            Confidence: {result.confidence.toFixed(2)}%
          </div>
        </div>

        <div className="transcriptBox" style={{ maxHeight: "160px", overflowY: "auto" }}>
          <h3 className="transcriptTitle" style={{ marginBottom: "12px", fontSize: "17px", color: "#111111", borderBottom: "1px solid rgba(0, 0, 0, 0.12)", paddingBottom: "8px" }}>
            Transcripts of Answers
          </h3>
          {answers && answers.length > 0 ? (
            answers.map((r, index) => (
              <div key={index} style={{ marginBottom: "10px", padding: "10px 12px", borderRadius: "10px", background: "rgba(0, 0, 0, 0.04)", borderLeft: "4px solid #111111", border: "1px solid rgba(0, 0, 0, 0.1)" }}>
                <div style={{ fontSize: "11px", color: "#111111", fontWeight: "700", textTransform: "uppercase", letterSpacing: "0.5px", marginBottom: "4px" }}>
                  Question {index + 1}: {r.question}
                </div>
                <div style={{ fontSize: "13.5px", color: "#111111", fontStyle: "italic", lineHeight: "1.4" }}>
                  "{r.transcript}"
                </div>
              </div>
            ))
          ) : (
            <p style={{ fontSize: "14px", color: "#555555", fontStyle: "italic" }}>No transcripts available.</p>
          )}
        </div>
      </div>

      <div className="resultsGrid">
        <div className="featuresBox">
          <h3 className="featuresTitle" style={{ marginBottom: "12px" }}>Extracted Linguistic Features</h3>
          <table>
            <thead>
              <tr>
                <th>Feature Description</th>
                <th style={{ textAlign: "right" }}>Analyzed Value</th>
              </tr>
            </thead>
            <tbody>
              {result.features && Object.entries(result.features).map(([key, val]) => (
                <tr key={key}>
                  <td style={{ textTransform: "capitalize" }}>
                    {key.replace(/_/g, " ")}
                  </td>
                  <td style={{ textAlign: "right", fontWeight: "600" }}>
                    {typeof val === "number" ? val.toFixed(3).replace(/\.?0+$/, "") : val}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <Visualization features={result.features} />
      </div>

    </div>
  );
}

export default ResultScreen;