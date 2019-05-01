import React from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";

const navDropdownTitle = user => {
  let title = "";

  if (!user) {
    title = " sign in";
  } else {
    title = ` ${user.username}`;
  }

  return title;
};

const FooskillNavbar = ({ user, signInHandle, signOutHandle }) => (
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
          {user && (
            <Nav.Link href="#submit">
              <FontAwesomeIcon icon="edit" /> add game
            </Nav.Link>
          )}
          <NavDropdown
            title={
              <span>
                <FontAwesomeIcon icon="cog" />
                {navDropdownTitle(user)}
              </span>
            }
            id="basic-nav-dropdown"
          >
            <NavDropdown.Item href={process.env.REACT_APP_FOOSKILL_ADMIN_URL}>
              Admin portal
            </NavDropdown.Item>
            <NavDropdown.Item href={process.env.REACT_APP_FOOSKILL_API_URL}>
              API root
            </NavDropdown.Item>
            <NavDropdown.Item
              href={process.env.REACT_APP_FOOSKILL_API_SPEC_URL}
            >
              API spec
            </NavDropdown.Item>
            <NavDropdown.Divider />
            {user ? (
              <NavDropdown.Item onClick={signOutHandle}>
                Sign out
              </NavDropdown.Item>
            ) : (
              <NavDropdown.Item onClick={signInHandle}>
                Sign in
              </NavDropdown.Item>
            )}
          </NavDropdown>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
);

export default FooskillNavbar;
