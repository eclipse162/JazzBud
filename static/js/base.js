document.addEventListener("DOMContentLoaded", () => {
  fetch("/spotify/user_info")
    .then((response) => response.json())
    .then((data) => {
      const usernameLink = document.getElementById("username-link");
      if (data && data.display_name) {
        usernameLink.textContent = '';
        const username = document.createElement("li");
        username.innerHTML = data.display_name;
        usernameLink.appendChild(username);
        //usernameLink.classList.add("username");
      }
    })
    .catch((error) => console.error("Error fetching user info:", error));
});
