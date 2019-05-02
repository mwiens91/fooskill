import React, { useContext, useEffect, useState } from "react";

import { ApiContext } from "./App";

const updatePlayers = async (api, setPlayers) => {
  const players = await api.getPlayers();
  setPlayers(players);
};

function Players() {
  const api = useContext(ApiContext);
  const [players, setPlayers] = useState(null);

  useEffect(() => {
    updatePlayers(api, setPlayers);
  }, [api]);

  return <div>{players && JSON.stringify(players)}</div>;
}

export default Players;
