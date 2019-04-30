import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";

const FooskillNavbar = ({ loggedIn, user }) => (
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
          <Nav.Link href="#submit">
            <FontAwesomeIcon icon="edit" /> add game
          </Nav.Link>
          <NavDropdown
            title={
              <span>
                <FontAwesomeIcon icon="cog" />
                {loggedIn ? (
                  <span> {user.username}</span>
                ) : (
                  <span> sign in</span>
                )}
              </span>
            }
            id="basic-nav-dropdown"
          >
            <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
            <NavDropdown.Item href="#action/3.2">
              Another action
            </NavDropdown.Item>
            <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item href="#action/3.4">
              Separated link
            </NavDropdown.Item>
          </NavDropdown>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
);

export default FooskillNavbar;
