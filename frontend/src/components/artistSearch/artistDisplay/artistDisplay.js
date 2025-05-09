import React, { useState, useEffect } from "react";
import { fetchInstrumentSearch } from "../../../api";

import InstrumentDropdown from "./instrumentDropdown/instrumentDropdown";
import styles from "./artistDisplay.module.css";

const ArtistDisplay = ({
  artist,
  onInstrument,
  onInstrumentRemove,
  onArtistRemove,
}) => {
  const [query, setQuery] = useState("");
  const [instruments, setInstruments] = useState([]);
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const [instrumentsVisible, setInstrumentsVisible] = useState(false);
  const [selectedInstruments, setSelectedInstruments] = useState([]);

  useEffect(() => {
    const fetchInstrumentData = async () => {
      if (query.length >= 3) {
        try {
          const data = await fetchInstrumentSearch(query);
          console.log(data.instrument_data);
          setInstruments(data.instrument_data);
          setDropdownVisible(true);
        } catch (error) {
          console.error("Error fetching instrument data:", error);
        }
      } else {
        setInstruments([]);
        setDropdownVisible(false);
      }
    };

    fetchInstrumentData();
  }, [query]);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleInstrumentSelect = (instrument) => {
    const existingInstrument = selectedInstruments.find(
      (inst) => inst.id === instrument.id
    );
    if (!existingInstrument) {
      setSelectedInstruments((prev) => [...prev, instrument]);
      setInstrumentsVisible(true);
    }
    setQuery("");
    setDropdownVisible(false);
    onInstrument(selectedInstruments);
  };

  const handleRemoveArtist = (artistId) => {
    onArtistRemove(artistId);
  };

  const handleRemoveInstrument = (instrumentId) => {
    setSelectedInstruments((prev) =>
      prev.filter((instrument) => instrument.id !== instrumentId)
    );
    onInstrumentRemove(instrumentId);
  };

  return (
    <div className={styles.artistDisplay}>
      <img
        src={artist.cover}
        alt={artist.name}
        className={styles.artistImage}
      />
      <div className={styles.artistInfo}>
        <div className={styles.artistName}>
          {artist.name}
          <button
            type="button"
            className={styles.removeArtist}
            onClick={() => handleRemoveArtist(artist.id)}>
            &times;
          </button>
        </div>

        <div className={styles.instrumentSearchContainer}>
          <div className={styles.selectedInstruments}>
            {instrumentsVisible &&
              selectedInstruments.map((instrument) => (
                <div
                  key={instrument.id}
                  className={styles.instrumentChip}
                  style={{
                    borderColor: instrument.colour,
                    color: instrument.colour,
                  }}>
                  <span>{instrument.name}</span>
                  <button
                    type="button"
                    className={styles.removeInstrument}
                    style={{ color: instrument.colour }}
                    onClick={() => handleRemoveInstrument(instrument.id)}>
                    &times;
                  </button>
                </div>
              ))}
          </div>

          <div className={styles.searchBox}>
            <input
              type="text"
              placeholder="Add Instrument"
              value={query}
              onChange={handleInputChange}
              className={styles.searchInput}
            />
            <button type="submit" className={styles.searchButton}>
              +
            </button>
          </div>

          {dropdownVisible && (
            <InstrumentDropdown
              instruments={instruments}
              onSelect={handleInstrumentSelect}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default ArtistDisplay;
