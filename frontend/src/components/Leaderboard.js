import React from "react";
import Spinner from "react-bootstrap/Spinner";
import Table from "react-bootstrap/Table";

const Leaderboard = ({ players }) => (
  <div>
    <h4>Top 10</h4>

    {players ? (
      <Table striped bordered hover size="sm">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Player</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          {players
            .sort((p1, p2) => p1.rating < p2.rating)
            .slice(0, 10)
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
          marginTop: "10em",
          justifyContent: "center"
        }}
      >
        <Spinner animation="border" />
      </div>
    )}
  </div>
);

export default Leaderboard;
