import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  useLocation,
} from "react-router-dom";
import Navigation from "./components/navigation";
import Home from "./pages/home";
import Login from "./pages/login";
import About from "./pages/about";
import Search from "./pages/search";
import "./styles/base.css";

const AppContent = () => {
  const location = useLocation();
  const hideNavigationRoutes = ["/login"];

  return (
    <>
      {/* Conditionally render Navigation */}
      {!hideNavigationRoutes.includes(location.pathname) && <Navigation />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/about" element={<About />} />
        <Route path="/search" element={<Search />} />
      </Routes>
    </>
  );
};

const App = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};

export default App;
