function authenticateSpotify(event) {
  event.preventDefault(); // Prevent the default action of the link

  fetch("/spotify/is-authenticated")
    .then((response) => response.json())
    .then((data) => {
      if (!data.status) {
        fetch("/spotify/auth")
          .then((response) => response.json())
          .then((data) => {
            window.location.href = data.url;
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      } else {
        window.location.href = "/home";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", () => {
  const loginButton = document.getElementById("spotify-login-button");
  if (loginButton) {
    loginButton.addEventListener("click", authenticateSpotify);
  } else {
  }
});
