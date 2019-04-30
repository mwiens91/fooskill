import React, { Component } from "react";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fab } from "@fortawesome/free-brands-svg-icons";
import {
  faChartBar,
  faCog,
  faEdit,
  faUserFriends
} from "@fortawesome/free-solid-svg-icons";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Leaderboard from "./Leaderboard";
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
      loggedIn: localStorage.getItem("token") ? true : false,
      players: null,
      user: null
    };

    this.handleSignIn = this.handleSignIn.bind(this);
    this.setLoggedIn = this.setLoggedIn.bind(this);
    this.setUserFromToken = this.setUserFromToken.bind(this);
  }

  handleSignIn = (e, data) => {
    e.preventDefault();

    this.Api.getApiTokenWithBasicAuth(data).then(json => {
      // TODO some error catching here if login no good
      this.setLoggedIn(json.token);
    });
  };

  setLoggedIn = token => {
    localStorage.setItem("token", token);
    this.setState({ logged_in: true });
  };
  setUserFromToken = token => {};

  async componentDidMount() {
    // Fetch list of players from API
    let players = await this.Api.getPlayers();
    this.setState({ players });

    // If logged in, get user info and give the token to the Api class
    if (this.state.loggedIn) {
      this.Api.setToken(localStorage.getItem("token"));

      let user = await this.Api.getUserFromApiToken();
      this.setState({ user });
    }
  }

  render() {
    // Make sure we have the basics loaded
    if (!this.state.players || (this.state.loggedIn && !this.state.user)) {
      return null;
    }

    return (
      <div className="App">
        <Navbar loggedIn={this.state.loggedIn} user={this.state.user} />

        <br />

        <Container>
          <Row>
            <Col>
              <Leaderboard players={this.state.players} />
            </Col>
            <Col>
              <SignInForm handleSubmit={this.handleSignIn} />
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default App;
