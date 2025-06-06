import { fetchArtist } from "../../api.js";
import { slugify } from "../../utils.js";
import { useNavigate } from "react-router-dom";

import styles from "./musicHeader.module.css";
import SpotifyPlayer from "../spotifyPlayer/spotifyPlayer.js";

const MusicHeader = ({ music, artistImage, token }) => {
  const navigate = useNavigate();
  const slugifiedArtist = slugify(music.artist);

  if (!music) {
    return <div>Request Not Found...</div>;
  }

  const handleArtist = async (artist_id, event) => {
    event.preventDefault();

    const data = await fetchArtist(artist_id);
    if (data) {
      navigate(`/artist/${slugifiedArtist}/${artist_id}`, {
        state: { results: data },
      });
    } else {
      console.error("No artist found");
    }
  };

  return (
    <main className={styles.page}>
      <div className={styles.header}>
        <div className={styles.content}>
          <div className={styles.coverContainer}>
            <img src={music.cover} alt={music.name} class={styles.cover} />
          </div>
          <div className={styles.info}>
            <h1 className={styles.title}>{music.title}</h1>
            <p className={styles.artist}>
              {artistImage && (
                <img
                  src={artistImage}
                  alt={music.artist}
                  class={styles.artistImage}
                />
              )}
              <div
                class={styles.clickable}
                onClick={(event) => handleArtist(music.artist_id, event)}>
                {music.artist}
              </div>
              &nbsp;&middot; {music.release_year}
            </p>
          </div>
          {/* {!artistImage && <SpotifyPlayer songID={music.id} token={token} />} */}
        </div>
      </div>
    </main>
  );
};

export default MusicHeader;
