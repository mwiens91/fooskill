import React, { useContext, useEffect, useState } from "react";

import { ApiContext } from "./App";

const updateTopPlayers = async (api, setTopPlayers) => {
  const topPlayers = await api.getTopNPlayers(100);
  setTopPlayers(topPlayers);
  localStorage.setItem("topPlayers", JSON.stringify(topPlayers));
};

const ratingDeltaDisplay = rating_delta => {
  const spanStyle = { "font-weight": "bold" };

  if (rating_delta === 0) {
    return (
      <span className="text-muted" style={spanStyle}>
        -
      </span>
    );
  } else if (rating_delta > 0) {
    return (
      <span className="text-success" style={spanStyle}>
        +{rating_delta}
      </span>
    );
  } else {
    return (
      <span className="text-warning" style={spanStyle}>
        {rating_delta}
      </span>
    );
  }
};

// Show a leaderboard (or spinner if the top players haven't loaded yet)
function Leaderboard() {
  const api = useContext(ApiContext);
  const [topPlayers, setTopPlayers] = useState(
    localStorage.getItem("topPlayers") !== null
      ? JSON.parse(localStorage.getItem("topPlayers"))
      : null
  );

  // Fetch and save list of top players from API
  useEffect(() => {
    updateTopPlayers(api, setTopPlayers);
  }, [api]);

  return (
    <div>
      <h4>Leaderboard</h4>

    </div>
  );
}

export default Leaderboard;
