import "../styles/search.module.css";
import "../styles/album_page.module.css";

import { useLocation } from "react-router-dom";
import { fetchArtist } from "../api.js";
import { useNavigate } from "react-router-dom";
import { slugify } from "../utils.js";
import TrackRow from "../components/trackRow/trackRow.js";

const Artist = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const { results } = location.state || {};
  const { album, artist_image } = results;
  const tracks = album.tracks;
  const slugifiedArtist = slugify(album.artist);

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
    <main className="album-page" style={{ padding: "40px" }}>
      <div className="album-header">
        <div className="album-content">
          <div className="album-cover-container">
            <img src={album.cover} alt={album.name} class="album-cover" />
          </div>
          <div className="album-info">
            <h1 className="album-title">{album.title}</h1>
            <p className="album-artist">
              <img src={artist_image} alt={album.artist} class="artist-image" />
              <div
                class="artist-link"
                onClick={(event) => handleArtist(album.artist_id, event)}>
                {album.artist}
              </div>
              &middot; {album.release_year}
            </p>
          </div>
        </div>
      </div>

      {/* Display Tracks */}

      <section
        className="track-list"
        style={{
          display: "flex",
          flexDirection: "column",
          paddingLeft: "12px",
        }}>
        {tracks && tracks.length > 0 ? (
          tracks.map((track) => <TrackRow key={track.id} track={track} />)
        ) : (
          <p>No tracks found</p>
        )}
      </section>
    </main>
  );
};

export default Artist;
