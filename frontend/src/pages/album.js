import { fetchAlbum } from "../api.js";
import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";

import TrackRow from "../components/trackRow/trackRow.js";
import MusicHeader from "../components/musicHeader/musicHeader.js";

const Album = () => {
  const location = useLocation();
  const { id: album_id } = useParams();
  const { results } = location.state || {};

  const [albumData, setAlbumData] = useState(results || null);
  const [loading, setLoading] = useState(!results);

  useEffect(() => {
    const fetchAlbumData = async () => {
      if (!results) {
        setLoading(true);
        try {
          const data = await fetchAlbum(album_id);
          setAlbumData(data);
        } catch (error) {
          console.error("Error fetching album data:", error);
        } finally {
          setLoading(false);
        }
      }
    };

    fetchAlbumData();
  }, [album_id, results]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (!albumData) {
    return <p>Album not found</p>;
  }

  const { album, artistImage, token } = albumData;
  const tracks = album.tracklist;

  return (
    <main className="album-page" style={{ padding: "40px" }}>
      <MusicHeader music={album} token={token} artistImage={artistImage} />

      <section
        className={"track-list"}
        style={{
          display: "flex",
          flexDirection: "column",
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
