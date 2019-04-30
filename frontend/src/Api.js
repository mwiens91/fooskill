class Api {
  constructor(baseApiUrl, token = null) {
    this.baseApiUrl = baseApiUrl;
    this.token = token;

    this.getApiTokenWithBasicAuth = this.getApiTokenWithBasicAuth.bind(this);
    this.getActivePlayers = this.getActivePlayers.bind(this);
    this.getUserFromApiToken = this.getUserFromApiToken.bind(this);
  }

  getApiTokenWithBasicAuth = authData =>
    fetch(`${this.baseApiUrl}/api-token-obtain/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(authData)
    })
      .then(response => response.json())
      .catch(error => error);

  getActivePlayers = () =>
    fetch(`${this.baseApiUrl}/players`)
      .then(response => response.json())
      .then(players => players.filter(p => p.is_active))
      .catch(error => error);

  getUser = username =>
    fetch(`${this.baseApiUrl}/users/${username}`)
      .then(response => response.json())
      .catch(error => error);

  getUserFromApiToken = () =>
    fetch(`${this.baseApiUrl}/api-token-current-user/${this.token}/`)
      .then(response => response.json())
      .catch(error => error);

  setToken = token => (this.token = token);
}

export default Api;
