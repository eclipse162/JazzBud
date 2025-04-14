import { deSlugify } from "../utils.js";
import { fetchSearch } from "../api.js";
import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";

import styles from "../styles/search.module.css";
import TrackRow from "../components/trackRow/trackRow.js";
import AlbumCard from "../components/albumCard/albumCard.js";
import ArtistCard from "../components/artistCard/artistCard";

const Search = () => {
  const location = useLocation();
  const { query: slugQuery } = useParams();
  const query = deSlugify(slugQuery);

  const { results } = location.state || {};

  const [searchData, setSearchData] = useState(results || null);
  const [loading, setLoading] = useState(!results);

  useEffect(() => {
    const fetchSearchData = async () => {
      if (!results) {
        setLoading(true);
        try {
          const data = await fetchSearch(query);
          setSearchData(data);
        } catch (error) {
          console.error("Error fetching album data:", error);
        } finally {
          setLoading(false);
        }
      }
    };

    fetchSearchData();
  }, [query, results]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (!searchData) {
    return <p>Album not found</p>;
  }

  const { tracks, albums, artists } = searchData;

  return (
    <main className={styles.searchPage}>
      <div className={styles.searchQuery}>
        <h2 className={styles.searchTitle}>Search Results for "{query}"</h2>
      </div>

      {/* Display Tracks */}

      <section className={styles.trackList}>
        {tracks && tracks.length > 0 ? (
          tracks.map((track) => (
            <TrackRow key={track.id} track={track} forAlbum={false} />
          ))
        ) : (
          <p>No tracks found</p>
        )}
      </section>

      {/* Display Artists */}
      <div className={styles.browseAllTitle}>Artists</div>
      <section className={styles.browseAll}>
        {artists && artists.length > 0 ? (
          artists.map((artist) => (
            <ArtistCard key={artist.id} artist={artist} />
          ))
        ) : (
          <p>No artists found</p>
        )}
      </section>

      {/* Albums */}
      <div className={styles.browseAllTitle}>Albums</div>
      <section className={styles.browseAll}>
        {albums && albums.length > 0 ? (
          albums.map((album) => <AlbumCard key={album.id} album={album} />)
        ) : (
          <p>No albums found</p>
        )}
      </section>
    </main>
  );
};

export default Search;
