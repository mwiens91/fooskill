import React from "react";
import Modal from "react-bootstrap/Modal";
import SignOutForm from "./SignOutForm";

const SignOutModal = ({ handleSubmit, onHide, show }) => (
  <Modal
    size="lg"
    aria-labelledby="contained-modal-title-vcenter"
    centered
    show={show}
    onHide={onHide}
  >
    <Modal.Header closeButton>
      <Modal.Title id="contained-modal-title-vcenter">Sign out</Modal.Title>
    </Modal.Header>
    <Modal.Body>
      <SignOutForm
        handleSubmit={e => {
          handleSubmit(e);
          onHide();
        }}
      />
    </Modal.Body>
  </Modal>
);

export default SignOutModal;
