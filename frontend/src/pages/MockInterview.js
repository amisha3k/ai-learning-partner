
import React, { useState } from "react";
import api from "../api";

export default function MockInterview() {
  const [file, setFile] = useState(null);
  const [role, setRole] = useState("");
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const startInterview = async () => {
    if (!file || !role) {
      setError("Please upload your resume and enter a role.");
      return;
    }

    setError("");
    setLoading(true);
    setQuestions([]);

    const formData = new FormData();
    formData.append("file", file); // matches FastAPI param
    formData.append("role", role);   // matches FastAPI param

    try {
      const res = await api.post("/api/mock_interview/start", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setQuestions(res.data.questions || []);
    } catch (err) {
      console.error(err);
      setError("Error communicating with interview bot.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <h2>🎤 Mock Interview</h2>

      <div className="mb-3">
        <input
          type="file"
          className="form-control mb-2"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <input
          type="text"
          className="form-control mb-2"
          placeholder="Enter role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />
        <button className="btn btn-primary" onClick={startInterview} disabled={loading}>
          {loading ? "Starting Interview..." : "Start Interview"}
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {questions.length > 0 && (
        <div className="mt-3">
          <h5>📄 Questions:</h5>
          <ol>
            {questions.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}
