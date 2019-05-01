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

    // Instance to make backend API calls with
    this.Api = new Api(process.env.REACT_APP_FOOSKILL_API_URL);

    // Some of these values are pulled from local storage to ensure that
    // page reloads are smooth. Generally they are recalculated after
    // the component mounts.
    this.state = {
      loggedIn:
        localStorage.getItem("loggedIn") !== null
          ? localStorage.getItem("loggedIn")
          : false,
      topPlayers:
        localStorage.getItem("topPlayers") !== null
          ? JSON.parse(localStorage.getItem("topPlayers"))
          : null,
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

  // Function passed to sign in form and called on form submission.
  handleSignIn = async (e, data) => {
    e.preventDefault();

    // This will throw an error if the request fails. Catch it!
    const tokenJson = await this.Api.getApiTokenWithBasicAuth(data);

    this.setLoggedIn({ token: tokenJson.token });
  };

  // Function passed to sign out form and called on form submission.
  handleSignOut = e => {
    e.preventDefault();
    this.setLoggedOut();
  };

  // Set the app to a logged-in state. Save the passed in API token to
  // local storage (provided we want to reset the API token), grab the
  // user corresponding to the API token we have (passed in or
  // otherwise), and flip the logged-in variable to true.
  setLoggedIn = async ({ token = null, setTokenInStorage = true }) => {
    // Optionally save the passed in token to local storage
    if (setTokenInStorage) {
      localStorage.setItem("token", token);
    }

    // Save the token on the API instance for convenient access
    if (token) {
      this.Api.setToken(token);
    } else {
      this.Api.setToken(localStorage.getItem("token"));
    }

    // Try fetching the user from the API token and update corresponding
    // variables. If fetching fails then reset these variables.
    try {
      // Fetch and set the user
      const user = await this.Api.getUserFromApiToken();

      this.setState({ loggedIn: true, user: user });

      // Store the login state to local storage
      localStorage.setItem("loggedIn", true);
      localStorage.setItem("user", JSON.stringify(user));
    } catch (e) {
      // Set the state of the app as logged-out (it probably is already
      // this way, but we'll make perform this action just in case)
      this.setLoggedOut();
    }
  };

  // Set the app to a logged-out state
  setLoggedOut = () => {
    // Set the state of the app as logged-out (it probably is already
    // this way, but we'll make perform this action just in case)
    this.setState({ loggedIn: false, user: null });

    // Reset the API instance's token
    this.Api.setToken(null);

    // Clear login-related variables from local storage
    localStorage.removeItem("token");
    localStorage.setItem("loggedIn", false);
    localStorage.setItem("user", null);
  };

  // Set whether to display the sign in modal
  setSignInModalOpen = truthVal => this.setState({ signInModalShow: truthVal });

  // Set whether to display the sign out modal
  setSignOutModalOpen = truthVal =>
    this.setState({ signOutModalShow: truthVal });

  // Do these this once when the component mounts: get players for the
  // leaderboard and perform a log-in action if there's a token in local
  // storage
  async componentDidMount() {
    // Fetch and save list of top players from API
    const topPlayers = await this.Api.getTopNPlayers();

    this.setState({ topPlayers });
    localStorage.setItem("topPlayers", JSON.stringify(topPlayers));

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
              <Leaderboard players={this.state.topPlayers} />
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
