import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";

const FooskillNavbar = () => (
  <Navbar bg="primary" variant="dark" expand="sm">
    <Container>
      <Navbar.Brand>fooskill</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href="#players">
            <FontAwesomeIcon icon="user-friends" /> players
          </Nav.Link>
          <Nav.Link href="#rankings">
            <FontAwesomeIcon icon="chart-bar" /> rankings
          </Nav.Link>
        </Nav>
        <Nav className="ml-auto">
          <Nav.Link href="#home">Submit game</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
);

export default FooskillNavbar;
