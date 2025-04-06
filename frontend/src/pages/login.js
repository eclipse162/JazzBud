import React from "react";
import "../styles/base.css";
import { isSpotifyAuthenticated, authenticateSpotify } from "../api";

const Login = () => {
  const handleSpotifyLogin = async (event) => {
    event.preventDefault();

    try {
      const authStatus = await isSpotifyAuthenticated();
      if (!authStatus.status) {
        const authData = await authenticateSpotify();
        window.location.href = authData.url;
      } else {
        window.location.href = "";
      }
    } catch (error) {
      console.error("Error during Spotify login flow:", error);
    }
  };

  return (
    <div>
      <div className="bg_img flex">
        <div className="taglines">
          <h1 id="jazzbud_tagline">
            A new way to share your favourite artists.
          </h1>
          <h2 id="jazzbud_desc">
            Find a song, view artist solos, vote on the best solo partitions,
            and so much more.
          </h2>
          <h2 id="jazzbud_desc2">
            Ready to get started? Register using your Spotify Premium account
            below.
          </h2>
          <button onClick={handleSpotifyLogin} className="btn btn-ghost">
            Log in with Spotify
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
