import React, { Component } from "react";
import PropTypes from "prop-types";

class SignInForm extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: "",
      password: ""
    };

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange = e => {
    this.setState({ [e.currentTarget.name]: e.currentTarget.value });
  };

  render() {
    return (
      <p>signmein</p>
    );
  }
}

export default SignInForm;

SignInForm.propTypes = {
  error: PropTypes.string,
  handleSubmit: PropTypes.func.isRequired
};
