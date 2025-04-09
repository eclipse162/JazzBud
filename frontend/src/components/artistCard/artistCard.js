import React from "react";
import { fetchArtist } from "../../api.js";
import { useNavigate } from "react-router-dom";
import { customSlugify } from "../../utils.js";
import "./artistCard.module.css";

const ArtistCard = ({ artist }) => {
  const slugifiedArtist = customSlugify(artist.name);
  const navigate = useNavigate();

  if (artist.name.length > 25) {
    artist.name = artist.name.substring(0, 25) + "...";
  }

  const handleArtist = async (artist_id, event) => {
    event.preventDefault();

    const data = await fetchArtist(artist_id);
    if (data) {
      navigate(`artist/${slugifiedArtist}/${artist_id}`, {
        state: { results: data },
      });
    } else {
      console.error("No artist found");
    }
  };

  return (
    <div
      className="artist-card"
      onClick={(event) => handleArtist(artist.artist_id, event)}>
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
    </div>
  );
};

export default ArtistCard;
