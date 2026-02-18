import { useEffect, useState } from "react";
import { getHome } from "./api";

function App() {
  const [review, setReview] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    console.log("Calling backend...");

    fetch("http://127.0.0.1:8000/latest-review")

      .then((res) => {
        if (!res.ok) throw new Error("Status " + res.status);
        return res.json();
      })
      .then((data) => {
        console.log("Received:", data);
        setReview(data);
      })
      .catch((err) => {
        console.error("Fetch failed:", err);
        setError(true);
      });
  }, []);

  if (error) return <h2 style={{ padding: 40 }}>❌ Cannot fetch AI review</h2>;
  if (!review) return <h2 style={{ padding: 40 }}>Loading AI Review...</h2>;

  return (
    <div style={{ padding: 40 }}>
      <h1>CodeRefine AI Dashboard 🚀</h1>
      <h2>Score: {review.score}</h2>

      <h3>Bugs</h3>
      <ul>{review.bugs.map((b, i) => <li key={i}>{b}</li>)}</ul>

      <h3>Security</h3>
      <ul>{review.security.map((s, i) => <li key={i}>{s}</li>)}</ul>

      <h3>Best Practices</h3>
      <ul>{review.best_practices.map((bp, i) => <li key={i}>{bp}</li>)}</ul>
    </div>
  );
}

export default App;