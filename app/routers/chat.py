from fastapi import APIRouter, Depends, HTTPException
from app.config import settings
from app.security import verify_api_key
from app.secret_ai_client import SecretAIClient
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS
from typing import Dict, List, Any
from app.models import AvailableModels

router = APIRouter()

chat_sessions: Dict[str, List[dict]] = {}

@router.get("/chat", tags=['Generation'])
async def chat_with_model(
    prompt: str,
    model: AvailableModels = AvailableModels.DEEPSEEK,
    api_key: str = Depends(verify_api_key)
):
    try:
        secret_client = SecretAIClient()
        
        session_id = f"session_{uuid5(NAMESPACE_DNS, api_key)}"
        
        system_prompt = """You are a thoughtful and helpful assistant when hlps user's whith their prompt/question. When answering user questions:
1. Take time to think carefully about the question
2. Consider multiple perspectives and approaches
3. Provide accurate, relevant, and complete information
4. Ensure your responses are clear and easy to understand
5. If you're uncertain about something, acknowledge it transparently
6. Use examples when it helps clarify your explanations
7. Remember previous parts of the conversation to maintain context
8. Ask clarifying questions if the user's request is ambiguous

Your goal is to provide the most helpful and satisfying response possible, ensuring the user's needs are fully addressed."""

        response = await secret_client.chat(model_name=model.value, prompt=prompt, system_prompt=system_prompt)
        
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        chat_sessions[session_id].append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        chat_sessions[session_id].append({
            "role": "assistant",
            "content": response.get("response", "Sorry, no response was generated."),
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "model": model,
            "response": response.get("response", "Sorry, no response was generated."),
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@router.get("/chat/history/{session_id}", tags=['History'])
async def get_chat_history(session_id: str, api_key: str = Depends(verify_api_key)):
    if session_id not in chat_sessions:
        return {"history": []}
    return {"history": chat_sessions[session_id]}