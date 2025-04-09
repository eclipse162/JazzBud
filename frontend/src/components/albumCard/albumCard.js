import React from "react";
import { fetchAlbum } from "../../api.js";
import { useNavigate } from "react-router-dom";
import { customSlugify } from "../../utils.js";
import "./albumCard.css";

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
      navigate(`artist/${slugifiedArtist}/${slugifiedTitle}/${album_id}`, {
        state: { results: data },
      });
    } else {
      console.error("No album found");
    }
  };

  return (
    <div
      className="album-card"
      onClick={(event) => handleAlbum(album.album_id, event)}>
      <img
        src={album.cover}
        alt={album.title}
        onError={(e) => {
          e.target.onerror = null;
          e.target.src = "/static/img/zanewins.jpeg";
        }}
      />
      <div className="album-info">
        <div className="album-title">{album.title}</div>
        <div className="album-artist">{album.artist}</div>
      </div>
    </div>
  );
};

export default AlbumCard;
