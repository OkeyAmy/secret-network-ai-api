import os

class Settings:
    SECRET_AI_API_KEY = os.getenv("SECRET_AI_API_KEY")
    API_KEY = os.getenv("API_KEY", "bWFzdGVyQHNjcnRsYWJzLmNvbTpTZWNyZXROZXR3b3JrTWFzdGVyS2V5X18yMDI1")
    CORS_ORIGINS = ["https://your-frontend-domain.com", "*"]
    
    # Define allowed origins for secure access without API key
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "your-frontend-domain.com,your-app.vercel.app").split(",")

settings = Settings()