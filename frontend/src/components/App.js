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
import Api from "../Api";

// Import FontAwesome stuff
library.add(fab, faChartBar, faCog, faEdit, faUserFriends);

class App extends Component {
  constructor(props) {
    super(props);

    this.Api = new Api(process.env.REACT_APP_FOOSKILL_API_URL);

    this.state = {
      displayedForm: null,
      loggedIn: localStorage.getItem("token") ? true : false,
      players: null,
      user: null
    };

    this.handleSignIn = this.handleSignIn.bind(this);
    this.setPlayers = this.setPlayers.bind(this);
    this.setUser = this.setUser.bind(this);
  }

  handleSignIn = (e, data) => {
    e.preventDefault();

    this.Api.getUserToken.then(json => {
      localStorage.setItem("token", json.token);

      console.log(json); // DEBUG

      this.setState({
        logged_in: true
      });
    });
  };

  setPlayers = players => this.setState({ players });
  setUser = user => this.setState({ user });

  componentDidMount() {
    // Fetch list of players from API
    this.Api.fetchPlayers().then(response => this.setPlayers(response));

    // If logged in, get user info
    if (this.state.loggedIn) {
      // stuff here
    }
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
          <SignInForm handleSubmit={this.handleSignIn} />
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
