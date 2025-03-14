import os

class Settings:
    SECRET_AI_API_KEY = os.getenv("SECRET_AI_API_KEY")
    API_KEY = os.getenv("API_KEY", "bWFzdGVyQHNjcnRsYWJzLmNvbTpTZWNyZXROZXR3b3JrTWFzdGVyS2V5X18yMDI1")
    CORS_ORIGINS = ["https://prompt-hub-silk.vercel.app", "*"]
    
    # Define allowed origins for secure access without API key
    # Default to the Vercel app and wildcard (*) if environment variable is not set
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://prompt-hub-silk.vercel.app,*").split(",")

settings = Settings()