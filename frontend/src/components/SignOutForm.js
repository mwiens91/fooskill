import React from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const SignOutForm = ({ handleSubmit }) => (
  <Form onSubmit={e => handleSubmit(e)}>
    <Button variant="primary" type="submit">
      Submit
    </Button>
  </Form>
);

export default SignOutForm;
