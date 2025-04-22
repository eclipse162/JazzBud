import React, { useState, useEffect } from "react";
import ArtistDropdown from "./artistDropdown/artistDropdown";
import ArtistDisplay from "./artistDisplay/artistDisplay";
import { fetchArtistSearch } from "../../api";

const ArtistSearch = ({ onArtistSelect }) => {
  const [query, setQuery] = useState(""); // Search query
  const [artists, setArtists] = useState([]); // List of artists fetched from the API
  const [dropdownVisible, setDropdownVisible] = useState(false); // Dropdown visibility
  const [selectedArtist, setSelectedArtist] = useState(null); // Selected artist

  useEffect(() => {
    const fetchSearchData = async () => {
      if (query.length >= 3) {
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
    onArtistSelect(artist);
  };

  return (
    <div className="artist-search-container">
      <input
        type="text"
        placeholder="Search"
        value={query}
        onChange={handleInputChange}
        className="artist-search"
      />

      {dropdownVisible && (
        <ArtistDropdown artists={artists} onSelect={handleArtistSelect} />
      )}

      {selectedArtist && <ArtistDisplay artist={selectedArtist} />}
    </div>
  );
};

export default ArtistSearch;
