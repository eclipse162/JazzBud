import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navigation from "./components/navigation";
import "./styles/base.css";

const App = () => {
  return (
    <Router>
      <Navigation />
    </Router>
  );
};

export default App;
