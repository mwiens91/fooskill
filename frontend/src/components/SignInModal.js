import React from "react";
import Modal from "react-bootstrap/Modal";
import SignInForm from "./SignInForm";

const SignInModal = ({ handleSubmit, onHide, show }) => (
  <Modal
    size="lg"
    aria-labelledby="contained-modal-title-vcenter"
    centered
    show={show}
    onHide={onHide}
  >
    <Modal.Header closeButton>
      <Modal.Title id="contained-modal-title-vcenter">Sign in</Modal.Title>
    </Modal.Header>
    <Modal.Body>
      <SignInForm
        handleSubmit={async (e, data) => {
          try {
            await handleSubmit(e, data);
            onHide();
          } catch (e) {
            console.log(e);
          }
        }}
      />
    </Modal.Body>
  </Modal>
);

export default SignInModal;
