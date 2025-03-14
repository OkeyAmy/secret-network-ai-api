# Secret Network AI Hub API

![Secret Network](https://secretnetwork.io/assets/images/Secret-Network-opengraph.png)

## Overview

The Secret Network AI Hub API is a powerful gateway to leverage Secret Network's advanced AI models in your applications. This API provides secure and private access to state-of-the-art language models including DeepSeek R1 (70B) and Llama 3.2 Vision, all running on the privacy-focused Secret Network blockchain infrastructure.

## Key Features

- **🤖 Advanced AI Models**: Access to DeepSeek R1 (70B) and Llama 3.2 Vision models
- **🔒 Privacy-Focused**: Built on Secret Network's privacy-preserving blockchain infrastructure
- **💬 Conversational AI**: Maintain chat sessions with context awareness
- **🖼️ Vision Capabilities**: Process and analyze images with multimodal models
- **✨ Prompt Engineering**: Tools to improve and optimize AI prompts
- **🔄 RESTful API**: Simple integration with any application using standard REST endpoints
- **📚 Comprehensive Documentation**: Detailed API documentation via Swagger UI and ReDoc

## Prerequisites

- Python 3.9+
- Secret AI API Key

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/secret-network-ai-api.git
cd secret-network-ai-api

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
# Windows PowerShell
$env:SECRET_AI_API_KEY="your_api_key_here"

# Windows CMD
set SECRET_AI_API_KEY=your_api_key_here

# Linux/Mac
export SECRET_AI_API_KEY="your_api_key_here"
```

## Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Models

- `GET /api/models` - Get available AI models
- `GET /api/model/{model_name}/capabilities` - Get detailed capabilities of a specific model

### Chat

- `GET /api/chat` - Chat with an AI model
  - Parameters:
    - `prompt`: The user's question or prompt
    - `model`: (Optional) The AI model to use

### Prompt Improvement

- `POST /api/improve-prompt` - Analyze and improve a user-provided prompt
  - Body:
    - `prompt`: The prompt text to improve

### Health Check

- `GET /api/health` - Check the health status of the API

## Usage Examples

### Chat with AI Model

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "http://localhost:8000"

headers = {
    "X-API-Key": API_KEY
}

response = requests.get(
    f"{BASE_URL}/api/chat",
    params={
        "prompt": "Explain the benefits of Secret Network for AI applications",
        "model": "deepseek-r1:70b"
    },
    headers=headers
)

print(response.json())
```

### Improve a Prompt

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "http://localhost:8000"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "prompt": "Create an image of a futuristic city"
}

response = requests.post(
    f"{BASE_URL}/api/improve-prompt",
    json=data,
    headers=headers
)

print(response.json())
```

## Deployment on Render

This project is set up for seamless deployment on Render with the API key pre-configured.

### Automatic Deployment

The easiest way to deploy is to use the included `render.yaml` file:

1. Create a new Render account or sign in at [dashboard.render.com](https://dashboard.render.com)
2. Click on the "New +" button and select "Blueprint"
3. Connect your GitHub/GitLab account and select your repository
4. Render will automatically detect the `render.yaml` file and set up your service
5. The environment variables, including the Secret AI API key, are already configured in the `render.yaml` file

### Manual Deployment

If you prefer to set up manually:

1. Create a new Web Service on Render
2. Connect to your repository
3. Use the following settings:
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add the environment variable:
   - Key: `SECRET_AI_API_KEY`
   - Value: `bWFzdGVyQHNjcnRsYWJzLmNvbTpTZWNyZXROZXR3b3JrTWFzdGVyS2V5X18yMDI1`

The API will be available at your Render URL once deployment is complete.

## Special Note for Frontend Engineers

This API has been configured for easy integration with frontend applications:

### Open Access API

For maximum convenience, this API is configured to accept requests from any origin without requiring authentication:

1. **No API Keys Required** - Frontend applications can make API calls without including any API keys or tokens.

2. **Simple Integration** - Just make standard fetch/axios calls from your frontend application:

```javascript
async function callSecretAI(prompt) {
  const response = await fetch('https://your-render-url.onrender.com/api/chat?prompt=' + encodeURIComponent(prompt));
  return await response.json();
}
```

### Security Note

The API still validates API keys if they are provided, but does not require them. This means:

- For public frontend applications: No authentication is needed
- For testing or backend integrations: You can still use API key authentication if desired

If using API key authentication, your requests would look like:

```javascript
async function callSecretAI(prompt) {
  const response = await fetch('https://your-render-url.onrender.com/api/chat?prompt=' + encodeURIComponent(prompt), {
    headers: {
      'X-API-Key': 'frontend-access-key-2025'
    }
  });
  return await response.json();
}
```

> **Note:** The backend already has the Secret Network AI API key configured, so you don't need to worry about that part of the authentication. Just focus on your frontend integration.

## Configuration

The API's configuration is managed through environment variables and the `app/config.py` file:

| Variable           | Description                                 | Default                        |
|--------------------|---------------------------------------------|--------------------------------|
| SECRET_AI_API_KEY  | API key for Secret Network AI               | (Pre-configured in render.yaml)|
| API_KEY            | Optional API key for authentication         | frontend-access-key-2025       |
| CORS_ORIGINS       | Allowed origins for CORS                    | ["*"] (All origins)           |
| ENVIRONMENT        | Current environment (production/dev)        | production                     |

## Project Structure

```
secret-network-ai-api/
├── app/
│   ├── __init__.py
│   ├── config.py         # Application configuration
│   ├── main.py           # Application entry point
│   ├── models.py         # Pydantic models
│   ├── security.py       # API security mechanisms
│   └── routers/          # API route handlers
│       ├── __init__.py
│       ├── chat.py       # Chat endpoint
│       ├── health.py     # Health check endpoint 
│       ├── model.py      # Model information endpoints
│       └── prompt_improver.py # Prompt improvement endpoint
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Dependencies

The key dependencies include:

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Secret AI SDK**: Official SDK for interacting with Secret Network AI models
- **Uvicorn**: ASGI server implementation for running the API

For a complete list, refer to the `requirements.txt` file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and further information about Secret Network's AI capabilities, visit [Secret Network](https://secretnetwork.io).

## Special Thanks

This project was created with love from Windsurf and Secret AI for their project. 

> **Note about API Keys:** The API key is open and publicly available. You can find it in the [Secret AI documentation](https://docs.secretnetwork.io/secret-network-documentation/secret-ai).

---

 2025 Secret Network AI Hub | Built with ❤️ by the Secret Network Community
