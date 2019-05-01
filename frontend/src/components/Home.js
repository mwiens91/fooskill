import React from "react";

import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

import Leaderboard from "./Leaderboard";

const Home = () => (
  <Row>
    <Col md={5}>
      <Leaderboard />
    </Col>
    <Col>
      <h4>STUFF HERE</h4>

      <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </p>
    </Col>
  </Row>
);

export default Home;
