import React, { useContext } from "react";
import { LinkContainer } from "react-router-bootstrap";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";

import { UserContext } from "./App";

const navDropdownTitle = user => {
  let title = "";

  if (!user) {
    title = " sign in";
  } else {
    title = ` ${user.username}`;
  }

  return title;
};

function FooskillNavbar({ signInHandle, signOutHandle }) {
  const user = useContext(UserContext);

  return (
    <Navbar bg="primary" variant="dark" expand="sm">
      <Container>
        <LinkContainer to="/">
          <Navbar.Brand>fooskill</Navbar.Brand>
        </LinkContainer>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <LinkContainer to="/players">
              <Nav.Link active={false}>
                <FontAwesomeIcon icon="user-friends" /> players
              </Nav.Link>
            </LinkContainer>
            <LinkContainer to="/rankings">
              <Nav.Link active={false}>
                <FontAwesomeIcon icon="chart-bar" /> rankings
              </Nav.Link>
            </LinkContainer>
          </Nav>
          <Nav className="ml-auto">
            {user && (
              <LinkContainer to="/submit">
                <Nav.Link active={false}>
                  <FontAwesomeIcon icon="edit" /> add game
                </Nav.Link>
              </LinkContainer>
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
}

export default FooskillNavbar;
