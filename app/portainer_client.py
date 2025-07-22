"""Portainer stack management utilities."""

import os
from typing import Dict, Any

import httpx


class PortainerClient:
    """Minimal Portainer API client."""

    def __init__(self) -> None:
        self.base_url = os.getenv("PORTAINER_URL")
        self.api_key = os.getenv("PORTAINER_API_KEY")

    def enabled(self) -> bool:
        return bool(self.base_url and self.api_key)

    async def restart_stack(self, stack_id: str) -> Dict[str, Any]:
        """Restart a Portainer stack."""
        url = f"{self.base_url}/api/stacks/{stack_id}/restart"
        headers = {"X-API-Key": self.api_key}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)
            response.raise_for_status()
            return {"message": f"Stack {stack_id} restarted"}
