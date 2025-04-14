import React from "react";
import { fetchLogin } from "../api";
import { useNavigate, useLocation } from "react-router-dom";
import "../styles/base.css";

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const redirectTo = location.state?.from || "/";

  const handleSpotifyLogin = async (event) => {
    event.preventDefault();

    const authStatus = await fetchLogin();
    if (authStatus?.status) {
      navigate(redirectTo);
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
