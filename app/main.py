import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings

# Load environment variables
load_dotenv()

# Set API key directly if not already set in environment
if not os.getenv("SECRET_AI_API_KEY"):
    os.environ['SECRET_AI_API_KEY'] = "bWFzdGVyQHNjcnRsYWJzLmNvbTpTZWNyZXROZXR3b3JrTWFzdGVyS2V5X18yMDI1"

# Initialize Secret client with the API key
from secret_ai_sdk.secret import Secret
secret_client = Secret()

# Verify API key is now available
secret_ai_api_key = os.getenv("SECRET_AI_API_KEY")
if not secret_ai_api_key:
    from secret_ai_sdk.secret_ai_ex import SecretAIAPIKeyMissingError
    raise SecretAIAPIKeyMissingError("Failed to set the SECRET_AI_API_KEY environment variable")

# Custom CORS middleware class
class CORSMiddlewareCustom(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Set CORS headers manually for all responses
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-API-Key"
        return response

def create_app():
    app = FastAPI(
        title="Secret Network AI Hub API",
        description="""API for integrating Secret Network's AI models with various applications. Access advanced language models securely through the Secret Network.""",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Add custom CORS middleware for maximum compatibility
    app.add_middleware(CORSMiddlewareCustom)
    
    # Standard CORS middleware as fallback (with fixed settings)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,  # Set to False when using wildcard
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add OPTIONS route handler for preflight requests
    @app.options("/{rest_of_path:path}")
    async def options_route(request: Request, rest_of_path: str):
        response = Response(status_code=200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-API-Key"
        return response

    # Import routers here to avoid circular imports
    from app.routers.model import router as models_router
    from app.routers.chat import router as chat_router
    from app.routers.prompt_improver import router as prompt_improver_router
    from app.routers.health import router as health_router
    
    app.include_router(models_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")
    app.include_router(prompt_improver_router, prefix="/api")
    app.include_router(health_router, prefix="/api")

    return app

app = create_app()