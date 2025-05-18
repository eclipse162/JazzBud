import React, { useState } from "react";
import { useLocation } from "react-router-dom";

import styles from "../styles/track.module.css";
import MusicHeader from "../components/musicHeader/musicHeader.js";
import ArtistSearch from "../components/artistSearch/artistSearch.js";
import Waveform from "../components/waveform/waveform.js";

const Track = () => {
  const location = useLocation();

  const { results } = location.state || {};
  const { track, token } = results;

  const [segments, setSegments] = useState({});
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

    setSegments((prev) => ({
      ...prev,
      [index]: [],
    }));
  };

  const handleAddSegment = (artistIndex, newSegment) => {
    setSegments((prev) => ({
      ...prev,
      [artistIndex]: [...(prev[artistIndex] || []), newSegment],
    }));
  };

  const handleUpdateSegment = (artistIndex, updatedSegments) => {
    setSegments((prev) => ({
      ...prev,
      [artistIndex]: updatedSegments,
    }));
  };

  const handleInstrumentSelect = (index, instrument) => {
    setArtistInstruments((prev) => {
      const updated = { ...prev };
      updated[index] = [...(updated[index] || []), instrument];
      return updated;
    });
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

    setSegments((prev) => {
      const updated = { ...prev };
      delete updated[index];
      return updated;
    });

    setArtistSearchComponents((prev) => prev.filter((i) => i !== index));
  };

  const handleRemoveInstrument = (index, instrumentId) => {
    setArtistInstruments((prev) => ({
      ...prev,
      [index]: prev[index].filter(
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
              <div key={index} className={styles.artistRow}>
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
                <div className={styles.waveformContainer}>
                  {selectedArtists[index] && (
                    <Waveform
                      artistIndex={index}
                      instruments={artistInstruments[index] || []}
                      segments={segments[index] || []}
                      songDuration={track.track_length}
                      onAddSegment={(newSegment) =>
                        handleAddSegment(index, newSegment)
                      }
                      onUpdateSegments={(updatedSegments) =>
                        handleUpdateSegment(index, updatedSegments)
                      }
                    />
                  )}
                </div>
              </div>
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
