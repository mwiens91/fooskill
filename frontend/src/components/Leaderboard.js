import React from "react";
import Spinner from "react-bootstrap/Spinner";
import Table from "react-bootstrap/Table";

// Show a leaderboard (or spinner if the top players haven't loaded yet)
const Leaderboard = ({ topPlayers }) => (
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
          {topPlayers
            .map((player, index) => (
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

export default Leaderboard;
