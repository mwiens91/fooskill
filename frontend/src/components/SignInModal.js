import React, { Component } from "react";
import Modal from "react-bootstrap/Modal";
import SignInForm from "./SignInForm";

class SignInModal extends Component {
  render() {
    return (
      <Modal
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
        show={this.props.show}
        onHide={this.props.onHide}
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">Sign in</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <SignInForm
            handleSubmit={(e, data) => {
              this.props.handleSubmit(e, data);
              this.props.onHide();
            }}
          />
        </Modal.Body>
      </Modal>
    );
  }
}

export default SignInModal;
