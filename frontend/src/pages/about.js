import { useEffect, useState } from "react";
import { fetchAboutMessage } from "../api";

function About() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchAboutMessage()
      .then((data) => setMessage(data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return <h1>{message || "Loading..."}</h1>;
}

export default About;
