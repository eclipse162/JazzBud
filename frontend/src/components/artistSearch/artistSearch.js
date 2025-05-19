import { fetchArtistSearch } from "../../api";
import React, { useState, useEffect } from "react";

import styles from "./artistSearch.module.css";
import ArtistDisplay from "./artistDisplay/artistDisplay";
import ArtistDropdown from "./artistDropdown/artistDropdown";

const ArtistSearch = ({ onArtistSelect, onRemoveArtist }) => {
  const [query, setQuery] = useState(""); // Search query
  const [debouncedQuery, setDebouncedQuery] = useState(""); // Debounced search query
  const [artists, setArtists] = useState([]); // List of artists fetched from the API
  const [dropdownVisible, setDropdownVisible] = useState(false); // Dropdown visibility
  const [searchVisible, setsearchVisible] = useState(true); // Search bar visibility
  const [selectedArtist, setSelectedArtist] = useState(null); // Selected artist

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(query);
    }, 300);

    return () => {
      clearTimeout(handler);
    };
  }, [query]);

  useEffect(() => {
    const fetchSearchData = async () => {
      if (debouncedQuery.length >= 3 && !selectedArtist) {
        try {
          const data = await fetchArtistSearch(debouncedQuery);
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
  }, [debouncedQuery, selectedArtist]);

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

  const handleArtistRemove = () => {
    setSelectedArtist(null);
    setsearchVisible(true);
    onRemoveArtist();
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
          onArtistRemove={handleArtistRemove}
        />
      )}
    </div>
  );
};

export default ArtistSearch;
