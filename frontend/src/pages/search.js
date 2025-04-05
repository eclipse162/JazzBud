import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { fetchSearch } from "../api"; // or wherever your api.js lives

import TrackRow from "./TrackRow";
import AlbumCard from "./AlbumCard";
import ArtistCard from "./ArtistCard";

const Search = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const query = queryParams.get("query");

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

  const { tracks } = results.tracks;
  const { albums } = results.albums;
  const { artists } = results.artists;

  return (
    <main className="search-page">
      <div className="search-query">
        <h2 className="search-title">Search Results for "{query}"</h2>
      </div>

      {/* Tracks */}
      <div className="divide-y divide-gray-800">
        <h3 className="text-xl font-semibold mt-6">Tracks</h3>
        {tracks && tracks.length > 0 ? (
          tracks.map((track) => <TrackRow key={track.id} track={track} />)
        ) : (
          <p>No tracks found</p>
        )}
      </div>

      {/* Artists */}
      <section>
        <h3>Artists</h3>
        {results.artists.map((artist) => (
          <div key={artist.artist_id}>{artist.name}</div>
        ))}
      </section>

      {/* Albums */}
      <section>
        <h3>Albums</h3>
        {results.albums.map((album) => (
          <div key={album.album_id}>
            {album.title} by {album.artist}
          </div>
        ))}
      </section>
    </main>
  );
};

export default Search;
