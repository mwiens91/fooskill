import React, { useContext, useEffect, useState } from "react";

import Spinner from "react-bootstrap/Spinner";
import Table from "react-bootstrap/Table";

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

      {topPlayers ? (
        <Table striped bordered hover size="sm">
          <thead>
            <tr>
              <th>Rank</th>
              <th style={{ "text-align": "center" }}>Δ</th>
              <th>Player</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            {topPlayers.map((player, index) => (
              <tr key={player.id}>
                <td>{player.ranking}</td>
                <td style={{ "text-align": "center" }}>
                  {ratingDeltaDisplay(player.ranking_delta)}
                </td>
                <td>{player.name}</td>
                <td>{Math.round(player.rating)}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      ) : (
        <div
          style={{
            display: "flex",
            marginRight: "4em",
            marginTop: "4em",
            marginBottom: "4em",
            justifyContent: "center"
          }}
        >
          <Spinner animation="border" />
        </div>
      )}
    </div>
  );
}

export default Leaderboard;
