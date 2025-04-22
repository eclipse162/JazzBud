import "../styles/search.module.css";
import "../styles/album_page.module.css";

import styles from "../styles/track.module.css";

import { useLocation } from "react-router-dom";
import MusicHeader from "../components/musicHeader/musicHeader.js";
import ArtistSearch from "../components/artistSearch/artistSearch.js";

const Track = () => {
  const location = useLocation();

  const { results } = location.state || {};
  const { track, token } = results;

  const handleArtistSelect = (artist) => {
    console.log("Selected Artist:", artist);
  };

  return (
    <main className={styles.page}>
      <MusicHeader music={track} artistImage={null} token={token} />

      <div className={styles.artistSection}>
        <div className={styles.artistTable}>
          <ArtistSearch onArtistSelect={handleArtistSelect} />
        </div>
      </div>
    </main>
  );
};

export default Track;
