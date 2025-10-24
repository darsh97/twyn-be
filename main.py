from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 👈 Import CORS
from typing import Dict
from api.v1.api import api_router

# --- Main FastAPI Application ---
app = FastAPI(
    title="Twynetic Orbit",
    description="Backend of Twynetic Orbit"
)

# ----------------------------------------------------
# 📌 CORS CONFIGURATION: ALLOWING ALL ORIGINS
# ----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 👈 Allows all origins
    allow_credentials=True,   # Allows credentials (cookies, auth headers)
    allow_methods=["*"],      # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],      # Allows all headers
)
# ----------------------------------------------------


# Include the v1 router in the main application
@app.get("/", response_model=Dict[str, str], include_in_schema=False)
async def read_root() -> Dict[str, str]:
    """
    Root endpoint for basic service verification.
    """
    return {"message": "Welcome to Twynetic Orbit API"}


app.include_router(api_router, prefix="/api/v1")