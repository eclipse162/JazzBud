import React, { useState } from "react";
import { useLocation } from "react-router-dom";

import styles from "../styles/track.module.css";
import MusicHeader from "../components/musicHeader/musicHeader.js";
import ArtistSearch from "../components/artistSearch/artistSearch.js";

const Track = () => {
  const location = useLocation();

  const { results } = location.state || {};
  const { track, token } = results;

  const [selectedArtists, setSelectedArtists] = useState([]);
  const [selectedInstruments, setSelectedInstruments] = useState([]);

  const handleArtistSelect = (artist) => {
    setSelectedArtists((prev) => [...prev, artist]);
  };

  const handleInstrumentSelect = (instruments) => {
    setSelectedInstruments((prev) => [...prev, instruments]);
  };

  return (
    <main className={styles.page} style={{ padding: "40px" }}>
      <MusicHeader music={track} artistImage={null} token={token} />

      <div className={styles.editContainer}>
        <div className={styles.artistSection}>
          <div className={styles.artistTable}>
            <ArtistSearch
              onArtistSelect={handleArtistSelect}
              onInstrumentSelect={handleInstrumentSelect}
            />
            <ArtistSearch
              onArtistSelect={handleArtistSelect}
              onInstrumentSelect={handleInstrumentSelect}
            />
            <ArtistSearch
              onArtistSelect={handleArtistSelect}
              onInstrumentSelect={handleInstrumentSelect}
            />
            <ArtistSearch
              onArtistSelect={handleArtistSelect}
              onInstrumentSelect={handleInstrumentSelect}
            />
          </div>
        </div>
      </div>
    </main>
  );
};

export default Track;
