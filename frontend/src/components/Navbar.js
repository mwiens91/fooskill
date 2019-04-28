import React from "react";
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
          <Nav.Link href="#features">Players</Nav.Link>
          <Nav.Link href="#pricing">Rankings</Nav.Link>
        </Nav>
        <Nav className="ml-auto">
          <Nav.Link href="#home">Submit game</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
);

export default FooskillNavbar;
