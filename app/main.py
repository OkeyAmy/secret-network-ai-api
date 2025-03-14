import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

def create_app():
    app = FastAPI(
        title="Secret Network AI Hub API",
        description="""API for integrating Secret Network's AI models with various applications. Access advanced language models securely through the Secret Network.""",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configure CORS - ensure it handles preflight requests correctly
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Use wildcard to allow all origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=86400,  # Cache preflight requests for 24 hours
    )

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