import React, { useContext } from "react";

import { UserContext } from "./App";

const navDropdownTitle = user => {
  let title = "";

  if (!user) {
    title = " sign in";
  } else {
    title = ` ${user.username}`;
  }

  return title;
};

function FooskillNavbar({ signInHandle, signOutHandle }) {
  const user = useContext(UserContext);

  return (
    <p>Hey</p>
  );
}

export default FooskillNavbar;
