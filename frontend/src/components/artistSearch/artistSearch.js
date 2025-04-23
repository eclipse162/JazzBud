import { fetchArtistSearch } from "../../api";
import React, { useState, useEffect } from "react";

import styles from "./artistSearch.module.css";
import ArtistDisplay from "./artistDisplay/artistDisplay";
import ArtistDropdown from "./artistDropdown/artistDropdown";

const ArtistSearch = ({
  onArtistSelect,
  onRemoveArtist,
  onInstrumentSelect,
  onRemoveInstrument,
}) => {
  const [query, setQuery] = useState(""); // Search query
  const [artists, setArtists] = useState([]); // List of artists fetched from the API
  const [selectedInstruments, setSelectedInstruments] = useState(null); // List of instruments an artist plays
  const [dropdownVisible, setDropdownVisible] = useState(false); // Dropdown visibility
  const [searchVisible, setsearchVisible] = useState(true); // Search bar visibility
  const [selectedArtist, setSelectedArtist] = useState(null); // Selected artist

  useEffect(() => {
    const fetchSearchData = async () => {
      if (query.length >= 3) {
        console.log(query);
        try {
          const data = await fetchArtistSearch(query);
          setArtists(data.artists);
          setDropdownVisible(true);
        } catch (error) {
          console.error("Error fetching artist data:", error);
        }
      } else {
        setArtists([]);
        setDropdownVisible(false);
      }
    };

    fetchSearchData();
  }, [query]);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleArtistSelect = (artist) => {
    setSelectedArtist(artist);
    setQuery(artist.name);
    setDropdownVisible(false);
    setsearchVisible(false);
    onArtistSelect(artist);
  };

  const handleInstrumentSelect = (instruments) => {
    setSelectedInstruments(instruments);
    onInstrumentSelect(instruments);
  };

  const handleArtistRemove = () => {
    setSelectedArtist(null);
    setsearchVisible(true);
    onRemoveArtist();
  };

  const handleInstrumentRemove = (instrumentId) => {
    setSelectedInstruments((prev) =>
      prev.filter((instrument) => instrument.id !== instrumentId)
    );
    onRemoveInstrument(instrumentId);
  };

  return (
    <div className={styles.artistSearchContainer}>
      {searchVisible && (
        <input
          type="text"
          placeholder="Search"
          value={query}
          onChange={handleInputChange}
          className={styles.artistSearch}
        />
      )}

      {dropdownVisible && (
        <ArtistDropdown artists={artists} onSelect={handleArtistSelect} />
      )}

      {selectedArtist && (
        <ArtistDisplay
          artist={selectedArtist}
          onInstrument={handleInstrumentSelect}
          onInstrumentRemove={handleInstrumentRemove}
          onArtistRemove={handleArtistRemove}
        />
      )}
    </div>
  );
};

export default ArtistSearch;
