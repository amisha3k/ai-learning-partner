import React, { useState } from "react";
import api from "../api";

export default function ATS() {
  const [jd, setJd] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const analyzeResume = async () => {
    if (!file || !jd) return;
    const formData = new FormData();
    formData.append("file", file);
    formData.append("jd", jd);

    try {
      const res = await api.post("/ats/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data.result);
    } catch (err) {
      console.error(err);
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
      <button className="btn btn-success" onClick={analyzeResume}>Analyze</button>
      {result && <div className="mt-3 p-3 border rounded bg-light"><pre>{result}</pre></div>}
    </div>
  );
}
