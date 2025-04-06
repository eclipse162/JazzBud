import { useEffect, useState } from "react";
import { fetchAbout } from "../api";

function About() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchAbout()
      .then((data) => setMessage(data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return <h1>{message || "Loading..."}</h1>;
}

export default About;
