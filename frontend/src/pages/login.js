import React, { useEffect } from "react";
import "../styles/login.css"; // Import your CSS file for styling
import "../styles/base.css"; // Import your global CSS file

const Login = () => {
  const authenticateSpotify = (event) => {
    event.preventDefault(); // Prevent the default action of the link

    fetch("/spotify/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        if (!data.status) {
          fetch("/spotify/auth")
            .then((response) => response.json())
            .then((data) => {
              window.location.href = data.url; // Redirect to Spotify login
            })
            .catch((error) => {
              console.error("Error:", error);
            });
        } else {
          window.location.href = "/core/home"; // Redirect to the home page
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  useEffect(() => {
    // Attaching event listener to the login button after the component mounts
    const loginButton = document.getElementById("spotify-login-button");
    if (loginButton) {
      loginButton.addEventListener("click", authenticateSpotify);
    }

    // Cleanup event listener on component unmount
    return () => {
      if (loginButton) {
        loginButton.removeEventListener("click", authenticateSpotify);
      }
    };
  }, []);

  return (
    <div>
      <div className="header">
        <h1 id="jazzbud_title">JazzBud</h1>
      </div>
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
          <button id="spotify-login-button" className="btn btn-ghost">
            Log in with Spotify
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
