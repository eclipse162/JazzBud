import React from "react";
import { Link } from "react-router-dom";
import { customSlugify } from "../../utils.js";
import "./artistCard.css";

const ArtistCard = ({ artist }) => {
  const slugifiedArtist = customSlugify(artist.name);

  return (
    <div className="artist-card">
      <Link to={`artist/${slugifiedArtist}/${artist.artist_id}`}>
        <img
          src={artist.cover}
          alt={artist.name}
          onError={(e) => {
            e.target.onerror = null;
            e.target.src = "/static/img/zanewins.jpeg";
          }}
        />
        <div className="artist-info">
          <div className="artist-name">{artist.name}</div>
          <div className="artist-title">Artist</div>
        </div>
      </Link>
    </div>
  );
};

export default ArtistCard;
