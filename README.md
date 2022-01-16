# REST Server Starter

Start a game server from a simple rest call!

This REST application allows you to setup multiple game server in a config file and start them from remote.

# Features
- Start a server process remotely
- Stop a server process remotely
- Automatically shutsdown after a timeout
- Webhooks!
	- On start
	- On stop
	- On about to shutdown aka reminder
- Organized games by versions

*Limited to run one server at a time.*

# Example request

**Start:**
```bash
curl --request POST \
  --url http://localhost:25575/server/start?game=<gameHere>&version=<versionHere> \
  --header 'Authorization: Bearer <tokenHere>' \
  --header 'Callback-Url: http://www.your-domain.com:8080/webhook'
```

**Stop:**
```bash
curl --request POST \
  --url http://localhost:25575/server/stop \
  --header 'Authorization: Bearer <tokenHere>'
```

**Reset timeout:**
```bash
curl --request POST \
  --url http://localhost:25575/server/resetTimeout \
  --header 'Authorization: Bearer <tokenHere>'
```