class Api {
  constructor(baseApiUrl, token = null) {
    this.baseApiUrl = baseApiUrl;
    this.token = token;

    this.fetchPlayers = this.fetchPlayers.bind(this);
  }

  getUserToken = data =>
    fetch(`${this.baseApiUrl}/api-token-auth/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    }).then(response => response.json());

  fetchPlayers = () =>
    fetch(`${this.baseApiUrl}/players`)
      .then(response => response.json())
      .catch(error => error);
}

export default Api;
