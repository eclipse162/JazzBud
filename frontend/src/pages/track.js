import "../styles/search.module.css";
import "../styles/album_page.module.css";

import { useLocation } from "react-router-dom";
import MusicHeader from "../components/musicHeader/musicHeader.js";

const Track = () => {
  const location = useLocation();

  const { results } = location.state || {};
  const { track, artistImage, token } = results;

  return (
    <main className="page" style={{ padding: "40px" }}>
      <MusicHeader music={track} artistImage={artistImage} token={token} />
    </main>
  );
};

export default Track;
