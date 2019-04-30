import React from "react";
import Table from "react-bootstrap/Table";

const FooskillLeaderboard = ({ players }) => (
  <div>
    <h2>PLAYAS</h2>

    <Table striped bordered hover size="sm">
      <thead>
        <tr>
          <th>rank</th>
          <th>name</th>
          <th>rating</th>
          <th>rating deviation</th>
        </tr>
      </thead>
      <tbody>
        {players
          .sort((p1, p2) => p1.rating < p2.rating)
          .map((player, index) => (
            <tr key={player.id}>
              <td>{index + 1}</td>
              <td>{player.name}</td>
              <td>{Math.round(player.rating)}</td>
              <td>{Math.round(player.rating_deviation)}</td>
            </tr>
          ))}
      </tbody>
    </Table>
  </div>
);

export default FooskillLeaderboard;
