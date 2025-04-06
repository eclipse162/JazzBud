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

    return await response.json(); // Return data to be used in components
  } catch (error) {
    console.error("Error searching songs:", error);
    return { error: "Failed to fetch search results." };
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
