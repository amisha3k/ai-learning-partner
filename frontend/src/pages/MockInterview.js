
// import React, { useState } from "react";
// import api from "../api";

// export default function MockInterview() {
//   const [file, setFile] = useState(null);
//   const [role, setRole] = useState("");
//   const [questions, setQuestions] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");

//   const startInterview = async () => {
//     if (!file || !role) {
//       setError("Please upload your resume and enter a role.");
//       return;
//     }

//     setError("");
//     setLoading(true);
//     setQuestions([]);

//     const formData = new FormData();
//     formData.append("file", file); // matches FastAPI param
//     formData.append("role", role);   // matches FastAPI param

//     try {
//       const res = await api.post("/api/mock_interview/start", formData, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });

//       setQuestions(res.data.questions || []);
//     } catch (err) {
//       console.error(err);
//       setError("Error communicating with interview bot.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="container mt-4">
//       <h2>🎤 Mock Interview</h2>

//       <div className="mb-3">
//         <input
//           type="file"
//           className="form-control mb-2"
//           onChange={(e) => setFile(e.target.files[0])}
//         />
//         <input
//           type="text"
//           className="form-control mb-2"
//           placeholder="Enter role"
//           value={role}
//           onChange={(e) => setRole(e.target.value)}
//         />
//         <button className="btn btn-primary" onClick={startInterview} disabled={loading}>
//           {loading ? "Starting Interview..." : "Start Interview"}
//         </button>
//       </div>

//       {error && <div className="alert alert-danger">{error}</div>}

//       {questions.length > 0 && (
//         <div className="mt-3">
//           <h5>📄 Questions:</h5>
//           <ol>
//             {questions.map((q, i) => (
//               <li key={i}>{q}</li>
//             ))}
//           </ol>
//         </div>
//       )}
//     </div>
//   );
// }

import React, { useState } from "react";
import api from "../api";

export default function MockInterview() {
  const [role, setRole] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const startInterview = async () => {
    try {
      const res = await api.post("/api/mock_interview/start", { role });
      setSessionId(res.data.session_id);
      setMessages([{ sender: "bot", text: res.data.response }]);
    } catch (err) {
      console.error(err);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { sender: "user", text: input }]);

    try {
      const res = await api.post("/api/mock_interview/chat", {
        session_id: sessionId,
        message: input,
      });

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: res.data.response },
      ]);
      if (res.data.end) setSessionId(""); // End session if stop/report used
    } catch (err) {
      console.error(err);
    }
    setInput("");
  };

  return (
    <div className="container mt-5">
      <h3 className="text-center mb-4">Mock Interview Assistant</h3>

      {!sessionId ? (
        <div className="text-center">
          <input
            type="text"
            className="form-control mb-3"
            placeholder="Enter Role (e.g., Data Scientist)"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          />
          <button className="btn btn-primary" onClick={startInterview}>
            Start Interview
          </button>
        </div>
      ) : (
        <>
          <div
            className="border p-3 mb-3 rounded"
            style={{ height: "400px", overflowY: "auto", background: "#f8f9fa" }}
          >
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`mb-2 ${
                  msg.sender === "bot" ? "text-primary" : "text-success text-end"
                }`}
              >
                <b>{msg.sender === "bot" ? "Interviewer: " : "You: "}</b>
                {msg.text}
              </div>
            ))}
          </div>

          <div className="d-flex">
            <input
              type="text"
              className="form-control me-2"
              placeholder='Type your answer or "start", "stop", "report"'
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <button className="btn btn-success" onClick={sendMessage}>
              Send
            </button>
          </div>
        </>
      )}
    </div>
  );
}
