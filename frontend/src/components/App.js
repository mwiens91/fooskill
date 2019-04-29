import React, { Component } from "react";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fab } from "@fortawesome/free-brands-svg-icons";
import {
  faChartBar,
  faCog,
  faEdit,
  faUserFriends
} from "@fortawesome/free-solid-svg-icons";
import Container from "react-bootstrap/Container";
import Table from "react-bootstrap/Table";
import Navbar from "./Navbar";
import SignInForm from "./SignInForm";

// Import FontAwesome stuff
library.add(fab, faChartBar, faCog, faEdit, faUserFriends);

const API_BASE_URL = process.env.REACT_APP_FOOSKILL_API_URL;

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      players: null
    };

    this.setPlayers = this.setPlayers.bind(this);
  }

  setPlayers(players) {
    this.setState({ players });
  }

  componentDidMount() {
    fetch(`${API_BASE_URL}/players`)
      .then(response => response.json())
      .then(response => this.setPlayers(response))
      .catch(error => error);
  }

  render() {
    const { players } = this.state;

    if (!players) {
      return null;
    }

    return (
      <div className="App">
        <Navbar />
        <Container>
          <br />
          <SignInForm handleSignIn={() => {}}/>
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
        </Container>
      </div>
    );
  }
}

export default App;
