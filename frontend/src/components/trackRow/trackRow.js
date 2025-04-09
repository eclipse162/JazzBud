import React from "react";
import { fetchTrack } from "../../api.js";
import { useNavigate } from "react-router-dom";
import { customSlugify, msToMinutesSeconds } from "../../utils.js";
import styles from "./trackRow.module.css";

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
    <div className={styles.trackRow}>
      <div
        className={styles.trackClickable}
        onClick={(event) => handleTrack(track.track_id, event)}>
        <img
          className={styles.trackCover}
          src={track.cover}
          alt={`${track.title} by ${track.artist}`}
        />
        <div className={styles.trackInfo}>
          <p className={styles.trackTitle}>{track.title}</p>
          <p className={styles.trackArtist}>{track.artist}</p>
        </div>
      </div>

      <div className={styles.trackLength}>
        <p>{trackLength}</p>
      </div>
    </div>
  );
};

export default TrackRow;
