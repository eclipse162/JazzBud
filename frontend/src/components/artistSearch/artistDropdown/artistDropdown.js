import React from "react";

const ArtistDropdown = ({ artists, onSelect }) => {
  if (!artists || artists.length === 0) return null;

  return (
    <div className="dropdown-container">
      {artists.map((artist) => (
        <div
          key={artist.artist_id}
          className="dropdown-item"
          onClick={() => onSelect(artist)}>
          <img src={artist.cover} alt={artist.name} className="artist-image" />
          <p>{artist.name}</p>
        </div>
      ))}
    </div>
  );
};

export default ArtistDropdown;
