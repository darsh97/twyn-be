from fastapi import APIRouter
from typing import Dict

# Define a router just for the endpoints in this file (e.g., all health-related routes)
router = APIRouter()

@router.get("/health", response_model=Dict[str, str], tags=["Health"])
async def get_health() -> Dict[str, str]:
    """
    Health check endpoint to confirm the API is running.
    The full path will be: /api/v1/health
    """
    return {"status": "ok"}