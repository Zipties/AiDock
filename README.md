# AiDock API

A small FastAPI server exposing Docker Swarm and optional Portainer management endpoints.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables:
   - `DOCKER_API_URL` (optional): Docker API base URL, otherwise defaults to environment configuration.
   - `PORTAINER_URL` and `PORTAINER_API_KEY` (optional): enable Portainer stack restart endpoint.
   - `API_TOKEN` (optional): token required in `X-Token` header for all endpoints.

3. Start the server:
   ```bash
uvicorn app.main:app --reload
```

## Docker

Build the image:

```bash
docker build -t aidock .
```

Run the container (mount the Docker socket if controlling the host):

```bash
docker run -p 8000:8000 -v /var/run/docker.sock:/var/run/docker.sock aidock
```

## Example `curl` commands

List services:
```bash
curl -H "X-Token: $API_TOKEN" http://localhost:8000/services
```

List containers:
```bash
curl -H "X-Token: $API_TOKEN" http://localhost:8000/containers
```

List nodes:
```bash
curl -H "X-Token: $API_TOKEN" http://localhost:8000/nodes
```

Scale a service:
```bash
curl -X POST -H "X-Token: $API_TOKEN" \
     "http://localhost:8000/service/<SERVICE_ID>/scale?replicas=3"
```

Update a service image:
```bash
curl -X POST -H "X-Token: $API_TOKEN" \
     "http://localhost:8000/service/<SERVICE_ID>/update?image=nginx:latest"
```

Remove a service:
```bash
curl -X POST -H "X-Token: $API_TOKEN" \
     http://localhost:8000/service/<SERVICE_ID>/remove
```

Restart a service:
```bash
curl -X POST -H "X-Token: $API_TOKEN" \
     http://localhost:8000/service/<SERVICE_ID>/restart
```

Get service logs:
```bash
curl -H "X-Token: $API_TOKEN" \
     "http://localhost:8000/service/<SERVICE_ID>/logs?tail=50"
```

Get container logs:
```bash
curl -H "X-Token: $API_TOKEN" \
     "http://localhost:8000/container/<CONTAINER_ID>/logs?tail=50"
```

Restart a Portainer stack (if configured):
```bash
curl -X POST -H "X-Token: $API_TOKEN" \
     http://localhost:8000/portainer/stack/<STACK_ID>/restart
```
