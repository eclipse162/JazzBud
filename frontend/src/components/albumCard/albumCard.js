import React from "react";
import { Link } from "react-router-dom";
import { customSlugify } from "../../utils.js";
import "./albumCard.css";

const AlbumCard = ({ album }) => {
  const slugifiedArtist = customSlugify(album.artist);
  const slugifiedTitle = customSlugify(album.title);

  if (album.title.length > 30) {
    album.title = album.title.substring(0, 30) + "...";
  }

  return (
    <div className="album-card">
      <Link to={`album/${slugifiedArtist}/${slugifiedTitle}/${album.album_id}`}>
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
      </Link>
    </div>
  );
};

export default AlbumCard;
