"""Simple token-based auth dependency for FastAPI."""

import os

from fastapi import Header, HTTPException

API_TOKEN = os.getenv("API_TOKEN", "")


async def verify_token(x_token: str = Header(...)) -> None:
    """Verify X-Token header matches API token."""
    if not API_TOKEN:
        return
    if x_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
