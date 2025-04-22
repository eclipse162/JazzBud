import React, { useState, useEffect } from "react";
import { fetchInstrumentSearch } from "../../api";

import InstrumentDropdown from "./instrumentDropdown/instrumentDropdown";
import styles from "./artistDisplay.module.css";

const ArtistDisplay = ({ artist }) => {
  const [query, setQuery] = useState("");
  const [instruments, setInstruments] = useState([]);
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const [instrumentsVisible, setInstrumentsVisible] = useState(false);
  const [selectedInstruments, setSelectedInstruments] = useState(null);

  useEffect(() => {
    const fetchInstrumentData = async () => {
      if (query.length >= 3) {
        try {
          const data = await fetchInstrumentSearch(query);
          setInstruments(data.instruments);
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
  };

  const handleRemoveInstrument = (instrumentId) => {
    setSelectedInstruments((prev) =>
      prev.filter((instrument) => instrument.id !== instrumentId)
    );
  };

  return (
    <div className={styles.artistDisplay}>
      <img src={artist.cover} alt={artist.name} className="artist-image" />
      <div className={styles.artistInfo}>
        <span className={styles.artistName}>{artist.name}</span>
      </div>

      <div className={styles.instrumentSearchContainer}>
        <div className={styles.selectedInstruments}>
          {instrumentsVisible &&
            selectedInstruments.map((instrument) => (
              <div
                key={instrument.id}
                className="instrument-chip"
                style={{ backgroundColor: instrument.color }}>
                <span>{instrument.name}</span>
                <button
                  type="button"
                  className="remove-instrument"
                  onClick={() => handleRemoveInstrument(instrument.id)}>
                  &times;
                </button>
              </div>
            ))}
        </div>

        <input
          type="text"
          placeholder="Search for instruments"
          value={query}
          onChange={handleInputChange}
          className={styles.instrumentSearch}
        />

        {dropdownVisible && (
          <InstrumentDropdown
            instruments={instruments}
            onSelect={handleInstrumentSelect}
          />
        )}
      </div>
    </div>
  );
};

export default ArtistDisplay;
