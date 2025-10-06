import React, { useState } from "react";
import api from "../api";

export default function ATS() {
  const [jd, setJd] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeResume = async () => {
    if (!file || !jd) {
      setError("Please provide both a resume and job description.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("jd", jd);

    try {
      const res = await api.post("/api/ats/analyze", formData, {  // <-- Fixed URL
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError("Error analyzing resume. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <h2>📄 ATS Resume Analyzer</h2>
      <textarea
        className="form-control mb-3"
        placeholder="Paste Job Description here..."
        rows="5"
        value={jd}
        onChange={(e) => setJd(e.target.value)}
      />
      <input
        type="file"
        className="form-control mb-3"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button className="btn btn-success" onClick={analyzeResume} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {error && <div className="mt-3 alert alert-danger">{error}</div>}

      {result && (
        <div className="mt-3 p-3 border rounded bg-light">
          <p>📊 Match Score: {result.percentage_match}%</p>
          <p>⭐ Overall Score: {result.overall_score}</p>
          <p>📝 Missing Keywords: {result.missing_keywords.length > 0 ? result.missing_keywords.join(", ") : "None"}</p>
          <p>🔧 Improvement Suggestions: {result.improvement_scope || "None"}</p>

          <p>📂 Sections Analysis:</p>
          {Object.keys(result.sections).length > 0 ? (
            <ul>
              {Object.entries(result.sections).map(([section, analysis]) => (
                <li key={section}>
                  <strong>{section}:</strong> Strength: {analysis.strength}, Reason: {analysis.reason}
                </li>
              ))}
            </ul>
          ) : (
            <p>No sections detected.</p>
          )}

          <p>⚠️ Grammar Issues:</p>
          {result.grammar_issues.length > 0 ? (
            <ul>{result.grammar_issues.map((issue, i) => <li key={i}>{issue}</li>)}</ul>
          ) : (
            <p>No grammar issues detected.</p>
          )}

          <p>🔁 Repetitive Words:</p>
          {result.repetitive_words.length > 0 ? (
            <ul>{result.repetitive_words.map((word, i) => <li key={i}>{word}</li>)}</ul>
          ) : (
            <p>None</p>
          )}
        </div>
      )}
    </div>
  );
}
