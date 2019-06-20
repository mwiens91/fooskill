import React, { useContext } from "react";
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';

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
    <div flexGrow="1">
      <AppBar position="static">
        <Toolbar>
          Jack
        </Toolbar>
      </AppBar>
    </div>
  );
}

export default FooskillNavbar;