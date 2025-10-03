import React, { useState } from "react";
import api from "../api";
import ChatMessage from "../components/ChatMessage";

export default function Tutor() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input) return;
    const userMsg = { role: "user", content: input };
    setMessages([...messages, userMsg]);

    try {
      const res = await api.post("/tutor/ask", {
        query: input,
        chat_history: messages.map(m => m.content),
      });
      const botMsg = { role: "assistant", content: res.data.answer };
      setMessages(prev => [...prev, userMsg, botMsg]);
    } catch (err) {
      console.error(err);
    }
    setInput("");
  };

  return (
    <div className="container mt-4">
      <h2>📘 AI Tutor</h2>
      <div className="chat-box border rounded p-3 mb-3" style={{ height: "400px", overflowY: "auto" }}>
        {messages.map((msg, i) => (
          <ChatMessage key={i} role={msg.role} content={msg.content} />
        ))}
      </div>
      <div className="d-flex">
        <input
          className="form-control me-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
        />
        <button className="btn btn-primary" onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
