import React from "react";
import { Link } from "react-router-dom";
import { customSlugify, msToMinutesSeconds } from "../../utils.js";
import "./trackRow.css";

const trackRow = ({ track }) => {
  const slugifiedTitle = customSlugify(track.title);
  const slugifiedArtist = customSlugify(track.artist);
  const trackLength = msToMinutesSeconds(track.track_length);

  return (
    <div className="track-row">
      <Link to={`track/${slugifiedArtist}/${slugifiedTitle}/${track.track_id}`}>
        <img
          className="track-cover"
          src={track.cover}
          alt={`${track.title} by ${track.artist}`}
        />
        <div className="track-info">
          <p className="track-title">{track.title}</p>
          <p className="track-artist">{track.artist}</p>
        </div>
      </Link>

      <div className="track-length">
        <p>{trackLength}</p>
      </div>
    </div>
  );
};

export default trackRow;
