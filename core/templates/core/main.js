import React, { Component } from "react";

export default class SimpleSpotifyAuth extends Component {
  constructor(props) {
    super(props);
    this.state = {
      spotifyAuthenticated: false,
    };
    this.authenticateSpotify = this.authenticateSpotify.bind(this);
  }

  componentDidMount() {
    this.authenticateSpotify();
  }

  authenticateSpotify() {
    fetch("/spotify/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ spotifyAuthenticated: data.status });
        console.log(data.status);
        if (!data.status) {
          fetch("/spotify/auth")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            });
        }
      });
  }

  render() {
    return (
      <div>
        {this.state.spotifyAuthenticated ? (
          <p>Spotify is authenticated</p>
        ) : (
          <p>Authenticating with Spotify...</p>
        )}
      </div>
    );
  }
}
