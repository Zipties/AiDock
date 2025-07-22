"""Docker Swarm management utilities."""

import os
from typing import Any, Dict, List, Optional

import docker
from docker.models.services import Service
from docker.models.containers import Container


def get_client() -> docker.DockerClient:
    """Create a Docker client based on environment variables."""
    base_url = os.getenv("DOCKER_API_URL")
    if base_url:
        return docker.DockerClient(base_url=base_url)
    return docker.from_env()


def list_services() -> List[Dict[str, Any]]:
    """List all services in the Swarm."""
    client = get_client()
    services = []
    for svc in client.services.list():
        attrs = svc.attrs
        services.append({
            "id": svc.id,
            "name": attrs.get("Spec", {}).get("Name"),
            "image": attrs.get("Spec", {}).get("TaskTemplate", {}).get("ContainerSpec", {}).get("Image"),
            "mode": attrs.get("Spec", {}).get("Mode"),
        })
    return services


def list_containers() -> List[Dict[str, Any]]:
    """List all containers."""
    client = get_client()
    containers = []
    for c in client.containers.list(all=True):
        containers.append({
            "id": c.id,
            "name": c.name,
            "status": c.status,
            "image": c.image.tags,
        })
    return containers


def list_nodes() -> List[Dict[str, Any]]:
    """List swarm nodes."""
    client = get_client()
    nodes = []
    for n in client.nodes.list():
        attrs = n.attrs
        nodes.append({
            "id": n.id,
            "hostname": attrs.get("Description", {}).get("Hostname"),
            "state": attrs.get("Status", {}).get("State"),
            "availability": attrs.get("Spec", {}).get("Availability"),
        })
    return nodes


def scale_service(service_id: str, replicas: int) -> Dict[str, Any]:
    """Scale a service to the specified number of replicas."""
    client = get_client()
    svc: Service = client.services.get(service_id)
    svc.scale(replicas)
    return {"message": f"Service {service_id} scaled to {replicas}"}


def update_service_image(service_id: str, image: str) -> Dict[str, Any]:
    """Update a service's image."""
    client = get_client()
    svc: Service = client.services.get(service_id)
    svc.update(image=image)
    return {"message": f"Service {service_id} updated to image {image}"}


def remove_service(service_id: str) -> Dict[str, Any]:
    """Remove a service."""
    client = get_client()
    svc: Service = client.services.get(service_id)
    svc.remove()
    return {"message": f"Service {service_id} removed"}


def restart_service(service_id: str) -> Dict[str, Any]:
    """Restart a service by updating it without changes."""
    client = get_client()
    svc: Service = client.services.get(service_id)
    svc.update(force_update=True)
    return {"message": f"Service {service_id} restarted"}


def service_logs(service_id: str, tail: int = 100) -> str:
    """Retrieve logs for a service."""
    client = get_client()
    svc: Service = client.services.get(service_id)
    return svc.logs(tail=tail, stdout=True, stderr=True).decode()


def container_logs(container_id: str, tail: int = 100) -> str:
    """Retrieve logs for a container."""
    client = get_client()
    ctr: Container = client.containers.get(container_id)
    return ctr.logs(tail=tail, stdout=True, stderr=True).decode()
