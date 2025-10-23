# File: app/api/v1/api.py

from fastapi import APIRouter
from .endpoints import health, contact

# The primary router for v1
api_router = APIRouter()

# Include the specific endpoint routers
api_router.include_router(health.router)
api_router.include_router(contact.router)