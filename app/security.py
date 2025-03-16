from fastapi import HTTPException, Request
from app.config import settings
import os

async def verify_api_key(request: Request):
    # Set SECRET_AI_API_KEY if not already set
    if not os.getenv("SECRET_AI_API_KEY"):
        os.environ['SECRET_AI_API_KEY'] = "bWFzdGVyQHNjcnRsYWJzLmNvbTpTZWNyZXROZXR3b3JrTWFzdGVyS2V5X18yMDI1"
    
    # Always return None to indicate no API key check
    return None