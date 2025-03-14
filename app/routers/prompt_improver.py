from fastapi import APIRouter, Depends, HTTPException, Body
from app.config import settings
from app.security import verify_api_key
from app.secret_ai_client import SecretAIClient
from pydantic import BaseModel
from typing import Dict, Any
from app.models import AvailableModels

router = APIRouter()
# System prompt for prompt improvement
PROMPT_IMPROVER_SYSTEM_PROMPT = """You are an expert prompt engineer specializing in improving prompts across all domains.
Your task is to:
1. Understand the user's intent from their prompt
2. Identify the most suitable category for the prompt
3. Apply category-specific best practices and improvements
4. Enhance the prompt while maintaining the original intent
5. Make it more effective, clear, and reliable

Focus on:
- Maintaining the user's core intent
- Adding necessary context and constraints
- Improving clarity and specificity
- Optimizing for the intended use case
- Adding error prevention
- Including relevant examples or format requirements
- Making it more reusable and flexible

Always return the improved prompt in a clear, ready-to-use format."""

class PromptRequest(BaseModel):
    prompt: str

@router.post("/improve-prompt", tags=["Prompt Improvement"])
async def improve_prompt(
    prompt: str = Body(..., description="The prompt text to improve"),
    api_key: str = Depends(verify_api_key)
) -> dict:
    try:
        # Create our custom client
        secret_client = SecretAIClient()
        
        # Use our simplified client to improve the prompt
        response = await secret_client.improve_prompt(prompt)
        
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
            
        # Return the improved prompt
        return {
            "original_prompt": prompt,
            "improved_prompt": response.get("response", "Sorry, no improved prompt was generated."),
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error improving prompt: {str(e)}")