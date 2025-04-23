import React from "react";
import styles from "../artistDisplay/artistDisplay.module.css";

const ArtistDropdown = ({ artists, onSelect }) => {
  if (!artists || artists.length === 0) return null;

  return (
    <div className={styles.dropdownContainer}>
      {artists.map((artist) => (
        <div
          key={artist.artist_id}
          onClick={() => onSelect(artist)}
          className={styles.dropdownItem}>
          <img
            src={artist.cover}
            alt={artist.name}
            className={styles.artistImage}
          />
          <p>{artist.name}</p>
        </div>
      ))}
    </div>
  );
};

export default ArtistDropdown;
