import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navigation from "./components/navigation";
import Home from "./pages/home";
import Login from "./pages/login";
import About from "./pages/about";
import Search from "./pages/search";
import "./styles/base.css";

const App = () => {
  return (
    <Router>
      <Navigation />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/about" element={<About />} />
        <Route path="/search" element={<Search />} />
        {/* Insert below */}
      </Routes>
    </Router>
  );
};

export default App;
