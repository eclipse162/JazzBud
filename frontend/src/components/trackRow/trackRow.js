import React from "react";
import { fetchTrack } from "../../api.js";
import { useNavigate } from "react-router-dom";
import { customSlugify, msToMinutesSeconds } from "../../utils.js";
import "./trackRow.module.css";

const TrackRow = ({ track }) => {
  const slugifiedTitle = customSlugify(track.title);
  const slugifiedArtist = customSlugify(track.artist);
  const trackLength = msToMinutesSeconds(track.track_length);
  const navigate = useNavigate();

  if (track.title.length > 60) {
    track.title = track.title.substring(0, 60) + "...";
  }

  const handleTrack = async (track_id, event) => {
    event.preventDefault();

    const data = await fetchTrack(track_id);
    if (data) {
      navigate(`track/${slugifiedArtist}/${slugifiedTitle}/${track_id}`, {
        state: { results: data },
      });
    } else {
      console.error("No album found");
    }
  };

  return (
    <div className="track-row">
      <div
        className="track-clickable"
        onClick={(event) => handleTrack(track.track_id, event)}>
        <img
          className="track-cover"
          src={track.cover}
          alt={`${track.title} by ${track.artist}`}
        />
        <div className="track-info">
          <p className="track-title">{track.title}</p>
          <p className="track-artist">{track.artist}</p>
        </div>
      </div>

      <div className="track-length">
        <p>{trackLength}</p>
      </div>
    </div>
  );
};

export default TrackRow;
