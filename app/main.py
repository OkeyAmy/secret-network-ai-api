import os 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Replace Secret AI SDK import with our custom client
from app.secret_ai_client import SecretAIClient

# Check API key
if not os.getenv("SECRET_AI_API_KEY"):
    raise ValueError("Please set the SECRET_AI_API_KEY environment variable")

def create_app():
    app = FastAPI(
        title="Secret Network AI Hub API",
        description="""API for integrating Secret Network's AI models with various applications. Access advanced language models securely through the Secret Network.""",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import routers here to avoid circular imports
    from app.routers import models_router, chat_router, prompt_improver_router, health_router
    
    app.include_router(models_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")
    app.include_router(prompt_improver_router, prefix="/api")
    app.include_router(health_router, prefix="/api")

    return app

app = create_app()