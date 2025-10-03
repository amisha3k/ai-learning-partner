import React from "react";

export default function ChatMessage({ role, content }) {
  const isUser = role === "user";
  return (
    <div className={`d-flex mb-2 ${isUser ? "justify-content-end" : "justify-content-start"}`}>
      <div className={`p-2 rounded ${isUser ? "bg-primary text-white" : "bg-light text-dark"}`}>
        {content}
      </div>
    </div>
  );
}
