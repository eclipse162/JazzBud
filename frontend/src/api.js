const API_BASE_URL = "https://jazzbud.onrender.com";

export const fetchHome = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}`, {
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching home data:", error);
    return { message: "Error loading data" };
  }
};

export const fetchAbout = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/about/`, {
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching about data:", error);
    return { message: "Error loading data" };
  }
};

export async function fetchSearch(query) {
  try {
    const response = await fetch(`${API_BASE_URL}/search/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ query }),
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error searching songs:", error);
    return { error: "Failed to fetch search results." };
  }
}

export async function fetchArtist(artistId) {
  try {
    const response = await fetch(`${API_BASE_URL}/artist/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ artistId }),
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error searching artist:", error);
    return { error: "Failed to fetch artist results." };
  }
}

export async function fetchAlbum(albumId) {
  try {
    const response = await fetch(`${API_BASE_URL}/album/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ albumId }),
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error searching album:", error);
    return { error: "Failed to fetch album results." };
  }
}

export async function fetchTrack(trackId) {
  try {
    const response = await fetch(`${API_BASE_URL}/track/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ trackId }),
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error searching album:", error);
    return { error: "Failed to fetch album results." };
  }
}

export const isSpotifyAuthenticated = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/spotify/is-authenticated`, {
      credentials: "include",
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    return await response.json();
  } catch (error) {
    console.error("Error checking Spotify authentication:", error);
    throw error;
  }
};

export const authenticateSpotify = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/spotify/auth`, {
      credentials: "include",
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    return await response.json();
  } catch (error) {
    console.error("Error initiating Spotify authentication:", error);
    throw error;
  }
};

export async function fetchSpotifyUserInfo() {
  try {
    const response = await fetch(`${API_BASE_URL}/spotify/user_info`, {
      credentials: "include",
      method: "GET",
    });

    if (!response.ok) {
      throw new Error("Failed to fetch Spotify user info");
    }

    const data = await response.json();

    if (data.error) {
      console.error("Error fetching user info:", data.error);
      return null;
    }
    return data;
  } catch (error) {
    console.error("Error fetching Spotify user info:", error);
    return null;
  }
}
