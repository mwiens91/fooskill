import React, { Component } from "react";
import PropTypes from "prop-types";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

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
      <Form onSubmit={e => this.props.handleSubmit(e, this.state)}>
        <h4>Sign in</h4>
        <Form.Group controlId="formUsername">
          <Form.Label>Username</Form.Label>
          <Form.Control
            name="username"
            onChange={this.handleChange}
            placeholder="Enter username"
          />
        </Form.Group>
        <Form.Group controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            name="password"
            onChange={this.handleChange}
            type="password"
            placeholder="Password"
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    );
  }
}

export default SignInForm;

SignInForm.propTypes = {
  handleSubmit: PropTypes.func.isRequired
};
