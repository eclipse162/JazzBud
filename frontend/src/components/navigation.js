import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { slugify } from "../utils.js";
import { fetchSpotifyUserInfo, fetchSearch } from "../api.js";

const Navigation = () => {
  const [query, setQuery] = useState("");
  const [displayName, setDisplayName] = useState("Username");
  const navigate = useNavigate();
  const location = useLocation();

  const querySlug = slugify(query);

  const handleSearch = async (event) => {
    event.preventDefault();

    const data = await fetchSearch(query);
    if (data.tracks || data.albums || data.artists) {
      navigate(`/search/${querySlug}`, {
        state: { results: data },
      });
    } else {
      console.error("No results found");
    }
  };

  useEffect(() => {
    const getUserInfo = async () => {
      const userInfo = await fetchSpotifyUserInfo();
      if (userInfo?.display_name) {
        setDisplayName(userInfo.display_name);
      } else {
        navigate(`/login`, {
          state: { from: location.pathname },
        });
      }
    };
    getUserInfo();
  }, [navigate, location]);

  return (
    <div className="page-container">
      <nav className="homepage_header">
        <div className="inner_header">
          <div className="logo_container">
            <a href="/">
              <img src="/img/logo.svg" alt="JazzBud" />
            </a>

            {/* Search Form */}
            <form onSubmit={handleSearch}>
              <div className="logo_container searchBox">
                <input
                  className="searchInput"
                  type="text"
                  name="query"
                  placeholder="Search"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit" className="searchButton">
                  <img src="/img/search.png" alt="Search" />
                </button>
              </div>
            </form>
          </div>

          {/* Navigation Links */}
          <ul className="navigation">
            <a href="/">
              <li>Home</li>
            </a>
            <a href="/about">
              <li>About</li>
            </a>
            <a href="/partitions">
              <li>My Partitions</li>
            </a>
            <a href="/profile">
              <li>{displayName}</li>
            </a>
          </ul>
        </div>
      </nav>
    </div>
  );
};

export default Navigation;
