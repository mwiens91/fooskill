import React, { Component } from "react";

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
      urls
    };
  }

  render() {
    return (
      <div className="App">
        <h1>FANTASTIC FOOSKILL FRONTEND</h1>
        {this.state.urls.map(item => (
          <div key={item.key}>
            <a href={item.url}>{item.title}</a>
          </div>
        ))}
      </div>
    );
  }
}

export default App;
