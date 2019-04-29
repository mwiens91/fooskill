import React, { Component } from "react";
import PropTypes from "prop-types";

class SignInForm extends Component {
  state = {
    username: "",
    password: ""
  };

  handleChange = e => {
    const name = e.target.name;
    const value = e.target.value;

    this.setState(prevState => {
      const newState = { ...prevState };
      newState[name] = value;
      return newState;
    });
  };

  render() {
    return (
      <form onSubmit={e => this.props.handleSignIn(e, this.state)}>
        <h4>sign in</h4>
        <label htmlFor="username">username</label>
        <input
          type="text"
          name="username"
          value={this.state.username}
          onChange={this.handleChange}
        />
        <label htmlFor="password">password</label>
        <input
          type="password"
          name="password"
          value={this.state.password}
          onChange={this.handleChange}
        />
        <input type="submit" />
      </form>
    );
  }
}

export default SignInForm;

SignInForm.propTypes = {
  handleSignIn: PropTypes.func.isRequired
};
