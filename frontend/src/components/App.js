import React, { Component } from "react";

const API_BASE_URL = process.env.REACT_APP_FOOSKILL_API_URL;

const urls = [
  {
    title: "admin page",
    url: process.env.REACT_APP_FOOSKILL_ADMIN_URL,
    key: 0
  },
  {
    title: "browsable API",
    url: process.env.REACT_APP_FOOSKILL_API_URL,
    key: 1
  },
  {
    title: "API specification",
    url: process.env.REACT_APP_FOOSKILL_API_SPEC_URL,
    key: 2
  }
];

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      players: null,
      urls: urls
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
        <h1>FANTASTIC FOOSKILL FRONTEND</h1>

        {this.state.urls.map(item => (
          <div key={item.key}>
            <a href={item.url}>{item.title}</a>
          </div>
        ))}

        <h2>PLAYAS</h2>

        {players
          .sort((p1, p2) => p1.rating < p2.rating)
          .map((player, index) => (
            <div key={player.id}>
              {index + 1}. {player.name} {Math.round(player.rating)}
            </div>
          ))}
      </div>
    );
  }
}

export default App;
