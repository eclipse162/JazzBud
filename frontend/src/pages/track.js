import React, { useState } from "react";
import { useLocation } from "react-router-dom";

import styles from "../styles/track.module.css";
import MusicHeader from "../components/musicHeader/musicHeader.js";
import ArtistSearch from "../components/artistSearch/artistSearch.js";

const Track = () => {
  const location = useLocation();
  const index = 0;

  const { results } = location.state || {};
  const { track, token } = results;

  const [selectedArtists, setSelectedArtists] = useState([]);
  const [artistInstruments, setArtistInstruments] = useState({});
  const [artistSearchComponents, setArtistSearchComponents] = useState([
    0, 1, 2, 3,
  ]);

  const handleArtistSelect = (index, artist) => {
    setSelectedArtists((prev) => {
      const updated = [...prev];
      updated[index] = artist;
      return updated;
    });

    setArtistInstruments((prev) => ({
      ...prev,
      [index]: [],
    }));
  };

  const handleInstrumentSelect = (index, instrument) => {
    setArtistInstruments((prev) => ({
      ...prev,
      [index]: [...(prev[index] || []), instrument],
    }));
  };

  const handleRemoveArtist = (index) => {
    setSelectedArtists((prev) => {
      const updated = [...prev];
      updated.splice(index, 1);
      return updated;
    });

    setArtistInstruments((prev) => {
      const updated = { ...prev };
      delete updated[index];
      return updated;
    });

    setArtistSearchComponents((prev) => prev.filter((i) => i !== index));
  };

  const handleRemoveInstrument = (artistId, instrumentId) => {
    setArtistInstruments((prev) => ({
      ...prev,
      [artistId]: prev[artistId].filter(
        (instrument) => instrument.id !== instrumentId
      ),
    }));
  };

  const handleAddArtistSearch = () => {
    setArtistSearchComponents((prev) => [...prev, prev.length]);
  };

  return (
    <main className={styles.page}>
      <MusicHeader music={track} artistImage={null} token={token} />

      <div className={styles.editContainer}>
        <div className={styles.artistSection}>
          <div className={styles.artistTable}>
            {artistSearchComponents.map((index) => (
              <ArtistSearch
                onArtistSelect={(artist) => handleArtistSelect(index, artist)}
                onInstrumentSelect={(instrument) =>
                  handleInstrumentSelect(index, instrument)
                }
                onRemoveInstrument={(instrumentId) =>
                  handleRemoveInstrument(index, instrumentId)
                }
                onRemoveArtist={() => handleRemoveArtist(index)}
              />
            ))}

            <button
              className={styles.addArtist}
              onClick={handleAddArtistSearch}>
              Add Artist
            </button>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Track;
