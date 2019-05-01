class Api {
  constructor(baseApiUrl, token = null) {
    this.baseApiUrl = baseApiUrl;
    this.token = token;

    this.getApiTokenWithBasicAuth = this.getApiTokenWithBasicAuth.bind(this);
    this.getActivePlayers = this.getActivePlayers.bind(this);
    this.getUser = this.getUser.bind(this);
    this.getUserFromApiToken = this.getUserFromApiToken.bind(this);
    this.setToken = this.setToken.bind(this);
  }

  // Get a list of active players
  getActivePlayers = () =>
    fetch(`${this.baseApiUrl}/players`)
      .then(response => response.json())
      .then(players => players.filter(p => p.is_active))
      .catch(error => error);

  // Get an API token by posting username and password. This will throw
  // an error if the request failed.
  getApiTokenWithBasicAuth = authData =>
    fetch(`${this.baseApiUrl}/api-token-obtain/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(authData)
    }).then(response => {
      if (!response.ok) {
        throw Error(response.statusText);
      }
      return response.json();
    });

  // Get the user corresponding to given a username
  getUser = username =>
    fetch(`${this.baseApiUrl}/users/${username}`)
      .then(response => response.json())
      .catch(error => error);

  // Get a user corresponding to a given API token. This will throw an
  // error if the request failed.
  getUserFromApiToken = () =>
    fetch(`${this.baseApiUrl}/api-token-current-user/${this.token}/`).then(
      response => {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response.json();
      }
    );

  // Set the API token for this instance
  setToken = token => (this.token = token);
}

export default Api;
