import React from "react";
import styles from "../../artistSearch/artistSearch.module.css";

const ArtistDropdown = ({ artists, onSelect }) => {
  if (!artists || artists.length === 0) return null;

  return (
    <div className={styles.dropdownContainer}>
      {artists.map((artist) => (
        <div
          key={artist.artist_id}
          className={styles.dropdownItem}
          onClick={() => onSelect(artist)}>
          <img src={artist.cover} alt={artist.name} className="artist-image" />
          <p>{artist.name}</p>
        </div>
      ))}
    </div>
  );
};

export default ArtistDropdown;
