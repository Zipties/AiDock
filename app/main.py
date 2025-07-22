"""FastAPI server exposing Docker Swarm management endpoints."""

from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException

from . import auth, docker_client
from .portainer_client import PortainerClient

app = FastAPI(title="AiDock API")


@app.get("/services", dependencies=[Depends(auth.verify_token)])
def get_services() -> Dict[str, Any]:
    """List Docker Swarm services."""
    try:
        return {"services": docker_client.list_services()}
    except Exception as exc:  # pragma: no cover - minimal error handling
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/containers", dependencies=[Depends(auth.verify_token)])
def get_containers() -> Dict[str, Any]:
    """List containers."""
    try:
        return {"containers": docker_client.list_containers()}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/nodes", dependencies=[Depends(auth.verify_token)])
def get_nodes() -> Dict[str, Any]:
    """List swarm nodes."""
    try:
        return {"nodes": docker_client.list_nodes()}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/service/{service_id}/scale", dependencies=[Depends(auth.verify_token)])
def scale_service(service_id: str, replicas: int) -> Dict[str, Any]:
    """Scale a service."""
    try:
        return docker_client.scale_service(service_id, replicas)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/service/{service_id}/update", dependencies=[Depends(auth.verify_token)])
def update_service(service_id: str, image: str) -> Dict[str, Any]:
    """Update a service's image."""
    try:
        return docker_client.update_service_image(service_id, image)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/service/{service_id}/remove", dependencies=[Depends(auth.verify_token)])
def remove_service(service_id: str) -> Dict[str, Any]:
    """Remove a service."""
    try:
        return docker_client.remove_service(service_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/service/{service_id}/restart", dependencies=[Depends(auth.verify_token)])
def restart_service(service_id: str) -> Dict[str, Any]:
    """Restart a service."""
    try:
        return docker_client.restart_service(service_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/service/{service_id}/logs", dependencies=[Depends(auth.verify_token)])
def service_logs(service_id: str, tail: int = 100) -> Dict[str, Any]:
    """Fetch logs for a service."""
    try:
        return {"logs": docker_client.service_logs(service_id, tail)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/container/{container_id}/logs", dependencies=[Depends(auth.verify_token)])
def container_logs(container_id: str, tail: int = 100) -> Dict[str, Any]:
    """Fetch logs for a container."""
    try:
        return {"logs": docker_client.container_logs(container_id, tail)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/portainer/stack/{stack_id}/restart", dependencies=[Depends(auth.verify_token)])
async def restart_stack(stack_id: str) -> Dict[str, Any]:
    """Restart a Portainer stack if Portainer is configured."""
    client = PortainerClient()
    if not client.enabled():
        raise HTTPException(status_code=400, detail="Portainer not configured")
    try:
        return await client.restart_stack(stack_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
