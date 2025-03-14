from fastapi import APIRouter, Depends, HTTPException, Body
from app.config import settings
from app.security import verify_api_key
from secret_ai_sdk.secret_ai import ChatSecret
from pydantic import BaseModel
from typing import Dict, Any
from app.models import AvailableModels

router = APIRouter()
# System prompt for prompt improvement
PROMPT_IMPROVER_SYSTEM_PROMPT = {
    "role": "system",
    "content": """You are an expert prompt engineer specializing in improving prompts across all domains.
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
}

class PromptRequest(BaseModel):
    prompt: str

@router.post("/improve-prompt", tags=["Prompt Improvement"])
async def improve_prompt(
    prompt: str = Body(..., description="The prompt text to improve"),
    api_key: str = Depends(verify_api_key)
) -> dict:
    try:
        from app.main import secret_client  # Import here to avoid circular imports
        
        urls = secret_client.get_urls(model=AvailableModels.DEEPSEEK)
        if not urls:
            raise HTTPException(status_code=404, detail="Model not found")
        secret_ai_llm = ChatSecret(
            base_url=urls[0],
            model=AvailableModels.DEEPSEEK,
            temperature=0.7
        )
        
        # improvement_prompt = # Construct the improvement request
        improvement_prompt = f"""You are a highly skilled prompt engineer with extensive experience in refining and optimizing prompts for clarity, effectiveness, and comprehensive coverage. Your task is to transform the following user prompt into a more detailed and actionable version while preserving its original intent.

USER PROMPT:
{prompt}

Instructions:

1. **Prompt Categorization:**  
   Analyze the provided prompt and select the most appropriate category from these options:


2. **Enhancement Objectives:**  
   Improve the prompt by incorporating the following enhancements:
   - **Clarity:** Ensure that every instruction is explicit and unambiguous.
   - **Specificity:** Include precise details that eliminate vagueness.
   - **Context:** Add any missing background or situational details to fully inform the responder.
   - **Constraints:** Introduce clear limitations or conditions to guide the response effectively.
   - **Usability:** Optimize the structure so the prompt is immediately actionable.
   - **Comprehensiveness:** Address all potential aspects of the prompt to make it as thorough as possible.
   - **Preservation of Intent:** Ensure that while making these improvements, the original purpose and intent of the prompt remain intact.
   - **Category-Specific Language:** Adapt the language based on the core purpose and content type of the prompt. For example, if the prompt involves NFT styling in digital art, include detailed references to NFT aesthetics, digital art techniques, generative art elements, and blockchain-inspired visuals. If the prompt is for text generation or persuasion, incorporate persuasive language, tone adjustments, or specific textual stylistic cues as needed. Ensure the improved prompt is tailored to the intended medium, whether image, text, or another format.

3. **Response Format:**  
   Format your response exactly as specified below without adding any extra text or commentary:
   
   
   [your enhanced version of the prompt]

Your response must follow this exact format and include only the necessary improvements as outlined. Do not include any additional explanations or commentary."""

        
        messages = [
            PROMPT_IMPROVER_SYSTEM_PROMPT,
            {"role": "user", "content": improvement_prompt}
        ]

        formatted_messages = [(msg["role"], msg["content"]) for msg in messages]
        response = secret_ai_llm.invoke(formatted_messages)
        
        # Parse the response
        content = response.content
        
        # Debug the actual content received
        print(f"Raw improve_prompt response content: {content}")
        
        if "<think>" in content and "</think>" in content:
            try:
                think_start = content.find("<think>") + len("<think>")
                think_end = content.find("</think>")
                think_output = content[think_start:think_end].strip()
                actual_response = content[content.find("</think>") + len("</think>"):].strip()
                
                # Return both parts separately
                return {
                    "Think Process": think_output,
                    "Response": actual_response
                }
            except Exception as parsing_error:
                print(f"Error parsing think tags: {parsing_error}")
                # Fall back to returning the whole response
                return {"response": content}
        else:
            # No think tags found, return the whole response
            return {"response": content}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error improving prompt: {str(e)}"
        )