import React from "react";
import { fetchAlbum } from "../../api.js";
import { useNavigate } from "react-router-dom";
import { customSlugify } from "../../utils.js";
import styles from "./albumCard.module.css";

const AlbumCard = ({ album }) => {
  const slugifiedArtist = customSlugify(album.artist);
  const slugifiedTitle = customSlugify(album.title);
  const navigate = useNavigate();

  if (album.title.length > 30) {
    album.title = album.title.substring(0, 30) + "...";
  }

  const handleAlbum = async (album_id, event) => {
    event.preventDefault();

    const data = await fetchAlbum(album_id);
    if (data) {
      navigate(`album/${slugifiedArtist}/${slugifiedTitle}/${album_id}`, {
        state: { results: data },
      });
    } else {
      console.error("No album found");
    }
  };

  console.log(styles);

  return (
    <div
      className={styles.albumCard}
      onClick={(event) => handleAlbum(album.album_id, event)}>
      <img
        src={album.cover}
        alt={album.title}
        onError={(e) => {
          e.target.onerror = null;
          e.target.src = "/static/img/zanewins.jpeg";
        }}
      />
      <div className={styles.albumInfo}>
        <div className={styles.albumTitle}>{album.title}</div>
        <div className={styles.albumArtist}>{album.artist}</div>
      </div>
    </div>
  );
};

export default AlbumCard;
