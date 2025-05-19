import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

import styles from "../styles/track.module.css";
import { useInstrumentContext } from "../components/contexts/InstrumentContext.js";
import MusicHeader from "../components/musicHeader/musicHeader.js";
import ArtistSearch from "../components/artistSearch/artistSearch.js";
import Waveform from "../components/waveform/waveform.js";
import { useSegmentContext } from "../components/contexts/SegmentContext.js";

const Track = () => {
  const location = useLocation();

  const { results } = location.state || {};
  const { track, token } = results;

  const [selectedArtists, setSelectedArtists] = useState([]);
  const [artistSearchComponents, setArtistSearchComponents] = useState([
    0, 1, 2, 3,
  ]);

  const { selectedInstruments } = useInstrumentContext();
  const { artistSegments, addSegment, removeSegment } = useSegmentContext();

  const handleArtistSelect = (index, artist) => {
    setSelectedArtists((prev) => {
      const updated = [...prev];
      updated[index] = artist;
      return updated;
    });

    addSegment((prev) => ({
      ...prev,
      [index]: [],
    }));
  };

  const handleRemoveArtist = (index) => {
    setSelectedArtists((prev) => {
      const updated = [...prev];
      updated.splice(index, 1);
      return updated;
    });

    artistSegments[index]?.forEach((segment) => {
      removeSegment(index, segment.id);
    });

    setArtistSearchComponents((prev) => prev.filter((i) => i !== index));
  };

  const handleAddSegment = (index, segment) => {
    addSegment(index, segment);
  };

  const handleRemoveSegment = (index, segmentId) => {
    removeSegment(index, segmentId);
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
                  index={index}
                  onArtistSelect={(artist) => handleArtistSelect(index, artist)}
                  onRemoveArtist={() => handleRemoveArtist(index)}
                />
                <div className={styles.waveformContainer}>
                  {selectedArtists[index] && (
                    <Waveform
                      songDuration={track.track_length}
                      instruments={selectedInstruments[index] || []}
                      artistSegments={artistSegments[index] || []}
                      addSegment={(segment) => handleAddSegment(index, segment)}
                      removeSegment={(segmentId) =>
                        handleRemoveSegment(index, segmentId)
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
