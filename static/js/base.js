document.addEventListener("DOMContentLoaded", () => {
  fetch("/spotify/user-info")
    .then((response) => response.json())
    .then((data) => {
      const usernameLink = document.getElementById("username-link");
      if (data && data.display_name) {
        usernameLink.textContent = data.display_name;
      }
    })
    .catch((error) => console.error("Error fetching user info:", error));
});
