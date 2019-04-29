class Api {
  constructor(baseApiUrl, token = null) {
    this.baseApiUrl = baseApiUrl;
    this.token = token;

    this.getApiTokenWithBasicAuth = this.getApiTokenWithBasicAuth.bind(this);
    this.getPlayers = this.getPlayers.bind(this);
    this.getUserFromApiToken = this.getUserFromApiToken.bind(this);
  }

  getApiTokenWithBasicAuth = authData =>
    fetch(`${this.baseApiUrl}/api-token-auth/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(authData)
    })
      .then(response => response.json())
      .catch(error => error);

  getPlayers = () =>
    fetch(`${this.baseApiUrl}/players`)
      .then(response => response.json())
      .catch(error => error);

  getUserFromApiToken = () =>
    fetch(`${this.baseApiUrl}/api-token-current-user/${this.token}`)
      .then(response => response.json())
      .catch(error => error);

  setToken = token => (this.token = token);
}

export default Api;
