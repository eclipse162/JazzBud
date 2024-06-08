let userID = "user-id";

async function getUserInfo(userID) {
  let response = await fetch("/api/user/info");
  let data = await response.json();
  return data;
}

let usernameLink = document.getElementById("username-link");
