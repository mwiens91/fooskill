import React, { useState } from "react";
import Modal from "react-bootstrap/Modal";
import SignInForm from "./SignInForm";

function SignInModal({ handleSubmit, onHide, show }) {
  const [error, setError] = useState(null);

  return (
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
          error={error}
          handleSubmit={async (e, data) => {
            try {
              await handleSubmit(e, data);
              setError(null);
              onHide();
            } catch (e) {
              setError("Login failed. Try again?");
            }
          }}
        />
      </Modal.Body>
    </Modal>
  );
}

export default SignInModal;
