let deviceId;
let isPlaying = false;
let currentTrackUri = null;
let currentPosition = 0;
let trackDuration = 0;
let progressInterval;

window.onSpotifyWebPlaybackSDKReady = () => {
  const token = window.spotifyAccessToken;
  const player = new Spotify.Player({
    name: "JBud Player",
    getOAuthToken: (cb) => {
      cb(token);
    },
    volume: 0.5,
  });

  player.connect().then((success) => {
    if (success) {
      console.log("The Web Playback SDK successfully connected to Spotify!");
    }
  });

  player.addListener("ready", ({ device_id }) => {
    console.log("Device ID:", device_id);
    fetch(`/core/transfer-playback/${device_id}/`);
  });

  player.addListener("player_state_changed", (state) => {
    if (!state) return;
    updateTrackInfo(state);
    startProgressUpdater(state);
  });
};

function updateTrackInfo(state) {
  const track = state.track_window.current_track;

  isPlaying = !state.paused;
  currentTrackUri = track.uri;
  trackDuration = state.duration;
  currentPosition = state.position;

  document.getElementById("duration").innerText = formatTime(trackDuration);
  document.getElementById("play-pause").innerText = isPlaying ? "⏸" : "▶️";
}

function togglePlayPause() {
  fetch(`/core/play/${currentTrackUri}/${isPlaying ? "pause" : "play"}/`)
    .then(() => {
      isPlaying = !isPlaying;
    })
    .catch((err) => console.error(err));
}

function startProgressUpdater(state) {
  clearInterval(progressInterval);
  if (!state.paused) {
    progressInterval = setInterval(() => {
      currentPosition += 1000;
      if (currentPosition >= trackDuration) clearInterval(progressInterval);

      document.getElementById("current-time").innerText =
        formatTime(currentPosition);
      const progressPercent = (currentPosition / trackDuration) * 100;
      document.getElementById("progress").style.width = progressPercent + "%";
    }, 1000);
  }
}

function formatTime(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
}

function seekTrack(event) {
  const progressBar = document.querySelector(".progress-bar");
  const clickPosition = event.offsetX / progressBar.clientWidth;
  const seekTo = trackDuration * clickPosition;

  fetch(
    `/core/play/${currentTrackUri}/position/?position_ms=${Math.floor(seekTo)}`
  )
    .then(() => (currentPosition = seekTo))
    .catch((err) => console.error(err));
}

document.addEventListener("htmx:afterSwap", (event) => {
  if (event.detail.target.id === "artist-results") {
    const results = event.detail.target.innerHTML;
    const dropdown = document.getElementById("artist-dropdown");
    dropdown.innerHTML = results;
    doocument.getElementById("artist-dropdown").classList.remove("hidden");
  }
});

document.addEventListener("click", (event) => {
  const target = event.target.closest(".dropdown-item");
  if (target) {
    const artistId = target.getAttribute("data-id");
    const artistName = target.getAttribute("data-name");
    const containerId = target.closest(".dropdown-container").id;

    const searchInput = document.querySelector(
      `input[hx-target="#${containerId}"]`
    );
    if (searchInput) {
      searchInput.value = artistName;
      searchInput.setAttribute("data-artist-id", artistId);
      sear;
      document.getElementById(containerId).classList.add("hidden");
    }
  }
});

document.getElementById("saveButton").addEventListener("click", () => {
  const rows = document.querySelectorAll(".editTable tr");
  const data = [];

  rows.forEach((row, index) => {
    const startTime = row.querySelector(".start-time").value;
    const endTime = row.querySelector(".end-time").value;

    // Match the artist search input for this row
    const artistSearchInput =
      document.querySelectorAll(".artist-search")[index];
    const artistId = artistSearchInput.getAttribute("data-artist-id");
    const songId = row.querySelector(".sp_song_id").value;

    if (artistId && startTime && endTime) {
      data.push({
        artist_id: artistId,
        start_time: startTime,
        end_time: endTime,
        sp_song_id: songId,
      });
    }
  });

  fetch("{% url 'save_artist_selection' %}", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": "{{ csrf_token }}",
    },
    body: JSON.stringify({ segments: data }),
  })
    .then((response) => {
      if (response.ok) {
        console.log("Segments saved successfully!");
      } else {
        console.error("Failed to save the segments.");
      }
    })
    .catch((error) => console.error("Error:", error));
});
