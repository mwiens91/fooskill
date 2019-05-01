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
import SignInModal from "./SignInModal";
import SignOutModal from "./SignOutModal";
import Api from "../Api";

// Import FontAwesome stuff
library.add(fab, faChartBar, faCog, faEdit, faUserFriends);

class App extends Component {
  constructor(props) {
    super(props);

    this.Api = new Api(process.env.REACT_APP_FOOSKILL_API_URL);

    this.state = {
      loggedIn:
        localStorage.getItem("loggedIn") !== null
          ? localStorage.getItem("loggedIn")
          : false,
      players: null,
      signInModalShow: false,
      signOutModalShow: false,
      user:
        localStorage.getItem("user") !== null
          ? JSON.parse(localStorage.getItem("user"))
          : null
    };

    this.handleSignIn = this.handleSignIn.bind(this);
    this.handleSignOut = this.handleSignOut.bind(this);
    this.setLoggedIn = this.setLoggedIn.bind(this);
    this.setLoggedOut = this.setLoggedOut.bind(this);
    this.setSignInModalOpen = this.setSignInModalOpen.bind(this);
    this.setSignOutModalOpen = this.setSignOutModalOpen.bind(this);
  }

  handleSignIn = async (e, data) => {
    e.preventDefault();

    // This will throw an error if the request fails
    const tokenJson = await this.Api.getApiTokenWithBasicAuth(data);

    this.setLoggedIn({ token: tokenJson.token });
  };

  handleSignOut = e => {
    e.preventDefault();
    this.setLoggedOut();
  };

  setLoggedIn = async ({ token = null, setTokenInStorage = true }) => {
    if (setTokenInStorage) {
      localStorage.setItem("token", token);
    }

    if (token) {
      this.Api.setToken(token);
    } else {
      this.Api.setToken(localStorage.getItem("token"));
    }

    try {
      const user = await this.Api.getUserFromApiToken();
      this.setState({ loggedIn: true, user: user });

      // Store these so next page reload is smoother. We'll still double
      // check these regardless when loading the page.
      localStorage.setItem("loggedIn", true);
      localStorage.setItem("user", JSON.stringify(user));
    } catch (e) {
      this.Api.setToken(null);
      localStorage.removeItem("token");

      // Store these so next page reload is smoother. Same reasoning as
      // comments above.
      localStorage.setItem("loggedIn", false);
      localStorage.setItem("user", false);
    }
  };

  setLoggedOut = () => {
    localStorage.removeItem("token");
    this.Api.setToken(null);
    this.setState({ loggedIn: false, user: null });
    localStorage.setItem("loggedIn", false);
    localStorage.setItem("user", false);
  };

  setSignInModalOpen = truthVal => this.setState({ signInModalShow: truthVal });

  setSignOutModalOpen = truthVal =>
    this.setState({ signOutModalShow: truthVal });

  async componentDidMount() {
    // Fetch list of players from API
    const players = await this.Api.getActivePlayers();
    this.setState({ players });

    // If there's a token stored, get user info and give the token to
    // the Api class
    if (localStorage.getItem("token")) {
      this.setLoggedIn({ setTokenInStorage: false });
    }
  }

  render() {
    return (
      <div className="App">
        <SignInModal
          show={this.state.signInModalShow}
          onHide={() => this.setSignInModalOpen(false)}
          handleSubmit={this.handleSignIn}
        />
        <SignOutModal
          show={this.state.signOutModalShow}
          onHide={() => this.setSignOutModalOpen(false)}
          handleSubmit={this.handleSignOut}
        />

        <Navbar
          loggedIn={this.state.loggedIn}
          user={this.state.user}
          signInHandle={() => this.setSignInModalOpen(true)}
          signOutHandle={() => this.setSignOutModalOpen(true)}
        />

        <br />

        <Container>
          <Row>
            <Col md={5}>
              <Leaderboard players={this.state.players} />
            </Col>
            <Col>
              <h4>STUFF HERE</h4>

              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
                in reprehenderit in voluptate velit esse cillum dolore eu fugiat
                nulla pariatur. Excepteur sint occaecat cupidatat non proident,
                sunt in culpa qui officia deserunt mollit anim id est laborum.
              </p>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default App;
