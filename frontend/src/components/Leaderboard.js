import React, { useContext, useEffect, useState } from "react";
import Spinner from "react-bootstrap/Spinner";
import Table from "react-bootstrap/Table";
import { ApiContext } from "./App";

const updateTopPlayers = async (api, setTopPlayers) => {
  const topPlayers = await api.getTopNPlayers();
  setTopPlayers(topPlayers);
  localStorage.setItem("topPlayers", JSON.stringify(topPlayers));
};

// Show a leaderboard (or spinner if the top players haven't loaded yet)
function Leaderboard() {
  const api = useContext(ApiContext);
  const [topPlayers, setTopPlayers] = useState(
    JSON.parse(localStorage.getItem("topPlayers"))
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
              <th>Player</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            {topPlayers.map((player, index) => (
              <tr key={player.id}>
                <td>{index + 1}</td>
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
