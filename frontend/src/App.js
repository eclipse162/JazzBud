import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  useLocation,
} from "react-router-dom";
import Navigation from "./components/navigation";
import { InstrumentProvider } from "./components/InstrumentContext";
import { SegmentProvider } from "./components/SegmentContext";
import Home from "./pages/home";
import Login from "./pages/login";
import About from "./pages/about";
import Search from "./pages/search";
import Artist from "./pages/artist";
import Album from "./pages/album";
import Track from "./pages/track";
import "./styles/base.css";

const AppContent = () => {
  const location = useLocation();
  const hideNavigationRoutes = ["/login"];

  console.log("Current location:", location.pathname);

  return (
    <>
      {!hideNavigationRoutes.includes(location.pathname) && <Navigation />}{" "}
      {/* ^^ Used to hide navbar on login ^^ */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/about" element={<About />} />
        <Route path="/search" element={<Search />} />
        <Route path="/artist/:slug/:id" element={<Artist />} />
        <Route path="/album/:artistslug/:titleslug/:id" element={<Album />} />
        <Route
          path="/track/:artistslug/:titleslug/:id"
          element={
            <SegmentProvider>
              <InstrumentProvider>
                <Track />
              </InstrumentProvider>
            </SegmentProvider>
          }
        />
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
