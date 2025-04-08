import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { fetchSearch } from "../api";
import { deSlugify } from "../utils.js";

import TrackRow from "../components/trackRow/trackRow.js";
import AlbumCard from "../components/albumCard/albumCard.js";
import ArtistCard from "../components/artistCard/artistCard";

import "../styles/search.css";

const Search = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const slugQuery = queryParams.get("query");
  const query = deSlugify(slugQuery);

  const [results, setResults] = useState({
    tracks: [],
    albums: [],
    artists: [],
  });

  useEffect(() => {
    const getSearchResults = async () => {
      const data = await fetchSearch(query);
      if (data.tracks) {
        setResults(data);
      } else {
        console.error("No results found");
      }
    };

    if (query) {
      getSearchResults();
    }
  }, [query]);

  const { tracks, albums, artists } = results;

  return (
    <main className="search-page">
      <div className="search-query">
        <h2 className="search-title">Search Results for "{query}"</h2>
      </div>

      {/* Display Tracks */}

      <section className="browse-all">
        <div className="track-list">
          {tracks && tracks.length > 0 ? (
            tracks.map((track) => <TrackRow key={track.id} track={track} />)
          ) : (
            <p>No tracks found</p>
          )}
        </div>
      </section>

      {/* Display Artists */}
      <div className="browse-all-title">Artists</div>
      <section className="browse-all">
        {artists && artists.length > 0 ? (
          artists.map((artist) => (
            <ArtistCard key={artist.id} artist={artist} />
          ))
        ) : (
          <p>No artists found</p>
        )}
      </section>

      {/* Albums */}
      <div className="browse-all-title">Albums</div>
      <section className="browse-all">
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
