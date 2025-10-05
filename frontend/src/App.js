// frontend/src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Tutor from "./pages/Tutor";
import ATS from "./pages/ATS";
import MockInterview from "./pages/MockInterview";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <Router>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">AI Learning Partner</Link>
          <div className="collapse navbar-collapse">
            <ul className="navbar-nav me-auto">
              <li className="nav-item">
                <Link className="nav-link" to="/tutor">Tutor</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/ats">ATS</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/mock">Mock Interview</Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<Tutor />} />
          <Route path="/tutor" element={<Tutor />} />
          <Route path="/ats" element={<ATS />} />
          <Route path="/mock" element={<MockInterview />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

