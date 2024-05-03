# PyDockerHub
Package provides some extended functionalities to 
[PyDockerHub API](https://docs.docker.com/docker-hub/api/latest/#tag/resources).
It doesn't cover all use cases, but rather focuses on managing images and builds during apps development.

## Installation
You can install `pydockerhub` with your favourite package managers:

pip:
```bash
pip install pydockerhub
```
poetry:
```bash
poetry add pydockerhub
```
## Extra Tricks
Official PyDockerHub API doesn't let you create or delete repositories, but you can do this through
the website. PyDockerHub simply adds some HTTP Headers to introduce itself as a user using web browser, rather than 
a program. It's not any kind of violation AFAIK but keep in mind, that this workaround might be disabled in the 
future.

## Credentials
You have basically two options when it comes to authenticating against DockerHub.

### Username and Password
The same you have used to create an account on DockerHub.

```json
{
  "username": "pinochcio",
  "password": "NoMoreLies"
}
```

### Username and Access Token
To obtain an `access_token` you have to generate it in your account settings section
[here](https://hub.docker.com/settings/security). By defining a proper scope you can generate Access Token without 
compromising your password when inviting collaborators. Then, you just use a `token as a password`:

```json
{
  "username": "pinochcio",
  "password": "dckr_pat_9QNXBGGtZt7(...)"
}
```

## Usage
