import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Tutor from "./pages/Tutor";
import ATS from "./pages/ATS";
import MockInterview from "./pages/MockInterview";

function App() {
  return (
    <Router>
      <div className="container mt-3">
        <nav className="mb-3">
          <Link className="btn btn-outline-primary me-2" to="/">Tutor</Link>
          <Link className="btn btn-outline-success me-2" to="/ats">ATS</Link>
          <Link className="btn btn-outline-warning" to="/mock">Mock Interview</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Tutor />} />
          <Route path="/ats" element={<ATS />} />
          <Route path="/mock" element={<MockInterview />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
