import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navigation from "./components/navigation";
import Home from "./pages/home";
import About from "./pages/about";
import Login from "./pages/login";
import Search from "./pages/search";
import "./styles/base.css";

const App = () => {
  return (
    <Router>
      <Navigation />
      <Routes>
        {/* Define all your main pages here */}
        <Route path="/" element={<Login />} /> {/* Home Page */}
        <Route path="/about" element={<About />} /> {/* About Page */}
        <Route path="/home" element={<Home />} /> {/* Login Page */}
        <Route path="/search" element={<Search />} /> {/* Search Page */}
        {/* Add other routes as needed */}
      </Routes>
    </Router>
  );
};

export default App;
