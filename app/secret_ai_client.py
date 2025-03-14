import requests
import os
import json

class SecretAIClient:
    """A simplified client to replace the secret-ai-sdk dependency for deployment"""
    
    def __init__(self):
        self.api_key = os.environ.get("SECRET_AI_API_KEY", "bWFzdGVyQHNjcnRsYWJzLmNvbTpTZWNyZXROZXR3b3JrTWFzdGVyS2V5X18yMDI1")
        self.base_url = "https://api.scrt.network/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def chat(self, model_name, prompt, system_prompt=None):
        """Send a chat request to the Secret AI API"""
        payload = {
            "model": model_name,
            "prompt": prompt,
        }
        
        if system_prompt:
            payload["system_prompt"] = system_prompt
            
        try:
            response = requests.post(
                f"{self.base_url}/chat", 
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "response": "Sorry, there was an error processing your request."}
    
    async def improve_prompt(self, prompt):
        """Send a prompt improvement request to the Secret AI API"""
        payload = {
            "prompt": prompt,
        }
            
        try:
            response = requests.post(
                f"{self.base_url}/improve-prompt", 
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "response": "Sorry, there was an error improving your prompt."}
