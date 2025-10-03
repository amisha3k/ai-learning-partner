import React, { useState } from "react";
import api from "../api";
import ChatMessage from "../components/ChatMessage";

export default function MockInterview() {
  const [resume, setResume] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const startInterview = async () => {
    if (!resume) return alert("Upload resume first!");
    const formData = new FormData();
    formData.append("resume", resume);
    try {
      const res = await api.post("/mock-interview/start", formData);
      setMessages([{ role: "assistant", content: res.data.message }]);
    } catch (err) {
      console.error(err);
    }
  };

  const sendAnswer = async () => {
    if (!input) return;
    const userMsg = { role: "user", content: input };
    setMessages([...messages, userMsg]);
    try {
      const res = await api.post("/mock-interview/answer", {
        answer: input,
        chat_history: messages.map(m => m.content),
      });
      const botMsg = { role: "assistant", content: res.data.response };
      setMessages(prev => [...prev, userMsg, botMsg]);
    } catch (err) {
      console.error(err);
    }
    setInput("");
  };

  return (
    <div className="container mt-4">
      <h2>🎤 Mock Interview</h2>
      {!resume && (
        <div>
          <input type="file" className="form-control mb-3" onChange={(e) => setResume(e.target.files[0])} />
          <button className="btn btn-primary" onClick={startInterview}>Start Interview</button>
        </div>
      )}
      <div className="chat-box border rounded p-3 mb-3" style={{ height: "400px", overflowY: "auto" }}>
        {messages.map((msg, i) => (
          <ChatMessage key={i} role={msg.role} content={msg.content} />
        ))}
      </div>
      {resume && (
        <div className="d-flex">
          <input
            className="form-control me-2"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Your answer..."
          />
          <button className="btn btn-primary" onClick={sendAnswer}>Send</button>
        </div>
      )}
    </div>
  );
}
