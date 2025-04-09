import React from "react";
import { Link } from "react-router-dom";
import { customSlugify } from "../../utils.js";
import "./artistCard.css";

const ArtistCard = ({ artist }) => {
  const slugifiedArtist = customSlugify(artist.name);

  if (artist.name.length > 25) {
    artist.name = artist.name.substring(0, 25) + "...";
  }

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
        </div>
      </Link>
    </div>
  );
};

export default ArtistCard;
