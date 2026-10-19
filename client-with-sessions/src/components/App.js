import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import Login from "../pages/Login";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/check_session")
      .then((r) => r.json())
      .then((user) => {
        setUser(user);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;

  if (!user || !user.id) {
    return <Login onLogin={setUser} />;
  }

  return (
    <>
      <NavBar user={user} setUser={setUser} />
      <main>
        <p>You are logged in!</p>
      </main>
    </>
  );
}

export default App;
