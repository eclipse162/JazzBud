import { useLocation } from "react-router-dom";
import TrackRow from "../components/trackRow/trackRow.js";
import MusicHeader from "../components/musicHeader/musicHeader.js";

const Album = () => {
  const location = useLocation();

  const { results } = location.state || {};
  const { album, artistImage, token } = results;
  const tracks = album.tracklist;

  return (
    <main className="album-page" style={{ padding: "40px" }}>
      <MusicHeader music={album} token={token} artistImage={artistImage} />

      <section
        className={"track-list"}
        style={{
          display: "flex",
          flexDirection: "column",
          paddingLeft: "12px",
        }}>
        {tracks && tracks.length > 0 ? (
          tracks.map((track) => (
            <TrackRow key={track.id} track={track} forAlbum={true} />
          ))
        ) : (
          <p>No tracks found</p>
        )}
      </section>
    </main>
  );
};

export default Album;
