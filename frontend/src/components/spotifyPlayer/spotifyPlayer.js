import styles from "./spotifyPlayer.module.css";
import React, { useEffect, useState, useCallback } from "react";

import { formatTime } from "../../utils.js";
import { transferPlayback } from "../../api.js";

const SpotifyPlayer = ({ songID, token, artistImage }) => {
  const [player, setPlayer] = useState(null);
  const [deviceId, setDeviceId] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTrackUri, setCurrentTrackUri] = useState(null);
  const [currentPosition, setCurrentPosition] = useState(0);
  const [trackDuration, setTrackDuration] = useState(0);
  const [progressInterval, setProgressInterval] = useState(null);

  const togglePlayPause = () => {
    if (!isPlaying && currentTrackUri && player) {
      player._options.getOAuthToken((token) => {
        fetch(
          `https://api.spotify.com/v1/me/player/play?device_id=${deviceId}`,
          {
            method: "PUT",
            body: JSON.stringify({ uris: [currentTrackUri] }),
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        ).then(() => {
          console.log(`Requested to play: ${currentTrackUri}`);
        });
      });
    } else if (player) {
      player.togglePlay().then(() => {
        console.log("Toggled playback!");
      });
    }
  };

  const seekTrack = (event) => {
    const progressBar = event.target;
    const clickPosition = event.nativeEvent.offsetX / progressBar.clientWidth;
    const seekTo = trackDuration * clickPosition;

    fetch(
      `/core/play/${currentTrackUri}/position/?position_ms=${Math.floor(
        seekTo
      )}`
    )
      .then(() => setCurrentPosition(seekTo))
      .catch((err) => console.error(err));
  };

  const updateTrackInfo = useCallback(
    (state) => {
      const track = state.track_window.current_track;

      setIsPlaying(!state.paused);
      setCurrentTrackUri(`spotify:track:${songID}`);
      setTrackDuration(state.duration);
      setCurrentPosition(state.position);

      console.log("Current track URI:", track.uri);
    },
    [songID]
  );

  const startProgressUpdater = useCallback(
    (state) => {
      clearInterval(progressInterval);
      if (!state.paused) {
        const interval = setInterval(() => {
          setCurrentPosition((prevPosition) => {
            const newPosition = prevPosition + 1000;
            if (newPosition >= trackDuration) clearInterval(interval);
            return newPosition;
          });
        }, 1000);
        setProgressInterval(interval);
      }
    },
    [progressInterval, trackDuration]
  );

  useEffect(() => {
    if (artistImage === null) {
      return null;
    }

    const script = document.createElement("script");
    script.src = "https://sdk.scdn.co/spotify-player.js";
    script.async = true;
    document.body.appendChild(script);

    window.onSpotifyWebPlaybackSDKReady = () => {
      const playerInstance = new window.Spotify.Player({
        name: "JBud Player",
        getOAuthToken: (cb) => {
          cb(token);
        },
        volume: 0.5,
      });

      setPlayer(playerInstance);

      playerInstance.connect().then((success) => {
        if (success) {
          console.log("Web Playback SDK successfully connected");
        }
      });

      playerInstance.addListener("ready", ({ device_id }) => {
        console.log("Device ID:", device_id);
        setDeviceId(device_id);
        transferPlayback(device_id);
      });

      playerInstance.addListener("player_state_changed", (state) => {
        if (!state) return;
        updateTrackInfo(state);
        startProgressUpdater(state);
      });
    };

    return () => {
      if (player) {
        player.disconnect();
      }
      document.body.removeChild(script);
    };
  }, [
    token,
    artistImage,
    songID,
    player,
    trackDuration,
    progressInterval,
    updateTrackInfo,
    startProgressUpdater,
  ]);

  return (
    <div className={styles.playerContainer}>
      <div className={styles.controls}>
        <button classname={styles.togglePlayPause} onClick={togglePlayPause}>
          {isPlaying ? "⏸️" : "▶️"}
        </button>
        <span className={styles.currentTime}>
          {formatTime(currentPosition)}
        </span>
        <div className={styles.progressWrapper}>
          <div className={styles.progressContainer}>
            <div
              className={styles.progressBar}
              onClick={seekTrack}
              style={{ position: "relative" }}>
              <div
                id="progress"
                className={styles.progress}
                style={{
                  width: `${(currentPosition / trackDuration) * 100}%`,
                }}></div>
            </div>
          </div>
          <span className={styles.duration}>{formatTime(trackDuration)}</span>
        </div>
      </div>
    </div>
  );
};

export default SpotifyPlayer;
