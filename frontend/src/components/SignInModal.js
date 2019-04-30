import React, { Component } from "react";
import Modal from "react-bootstrap/Modal";
import SignInForm from "./SignInForm";

class SignInModal extends Component {
  render() {
    return (
      <Modal
        {...this.props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">Sign in</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <SignInForm handleSubmit={this.props.handleSubmit} />
        </Modal.Body>
      </Modal>
    );
  }
}

export default SignInModal;
