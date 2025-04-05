import { useEffect, useState } from "react";
import { fetchHomeMessage } from "../api";

function Home() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchHomeMessage()
      .then((data) => setMessage(data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return <h1>{message || "Loading..."}</h1>;
}

export default Home;
