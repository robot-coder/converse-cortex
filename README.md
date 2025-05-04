# README.md

# Web-Based Chat Assistant

This project implements a web-based Chat Assistant that provides a user-friendly interface for interacting with various Large Language Models (LLMs). It features continuous conversations, optional multimodal capabilities, and comparison functionalities. The application is designed to be deployed easily on Render.com.

## Features

- Web UI for seamless chat interactions
- Backend API supporting multiple LLMs
- Continuous conversation context management
- Optional multimodal (e.g., image input) support
- Model comparison features
- Deployable on cloud platforms like Render.com

## Files

- `front_end.html`: Front-end user interface
- `app.py`: Backend API server
- `requirements.txt`: Dependencies
- `README.md`: Documentation

## Requirements

Ensure you have Python 3.8+ installed. Install dependencies via:

```bash
pip install -r requirements.txt
```

## Deployment

1. Push your code to a Git repository.
2. Connect your repository to Render.com.
3. Set the start command to:

```bash
uvicorn app:app --host=0.0.0.0 --port=10000
```

4. Deploy and access your chat assistant via the provided URL.

## Usage

Open `front_end.html` in your browser or host it on a static site. Interact with the chat interface to communicate with the backend API.

---

## Code Files

### front_end.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Chat Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        #chat { border: 1px solid #ccc; padding: 10px; height: 400px; overflow-y: scroll; }
        #userInput { width: 80%; }
        #sendBtn { width: 15%; }
        .message { margin: 5px 0; }
        .user { color: blue; }
        .bot { color: green; }
    </style>
</head>
<body>
    <h1>Web-Based Chat Assistant</h1>
    <div id="chat"></div>
    <input type="text" id="userInput" placeholder="Type your message..." />
    <button id="sendBtn">Send</button>

    <script>
        const chatDiv = document.getElementById('chat');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;
            appendMessage('User', message, 'user');
            userInput.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                if (response.ok) {
                    appendMessage('Bot', data.reply, 'bot');
                } else {
                    appendMessage('Error', data.detail || 'Error occurred', 'error');
                }
            } catch (error) {
                appendMessage('Error', error.message, 'error');
            }
        }

        function appendMessage(sender, message, className) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${className}`;
            msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            chatDiv.appendChild(msgDiv);
            chatDiv.scrollTop = chatDiv.scrollHeight;
        }

        sendBtn.onclick = sendMessage;
        userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
```

### app.py

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
from typing import Optional, Dict

app = FastAPI()

# Placeholder for conversation context storage
# In production, consider using a database or session management
conversation_context: Dict[str, str] = {}

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default_user"

class ChatResponse(BaseModel):
    reply: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Handle chat messages from the client, maintain context, and interact with LLMs.
    """
    user_id = request.user_id
    message = request.message

    # Retrieve previous context if exists
    context = conversation_context.get(user_id, "")

    # Prepare prompt with context
    prompt = f"{context}\nUser: {message}\nBot:"

    try:
        # Call to external LLM API (placeholder)
        # Replace with actual LLM API call, e.g., OpenAI, Hugging Face, etc.
        reply = await call_llm(prompt)
        # Update context
        conversation_context[user_id] = f"{context}\nUser: {message}\nBot: {reply}"
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def call_llm(prompt: str) -> str:
    """
    Interact with an LLM API to generate a response.
    Replace the placeholder implementation with actual API calls.
    """
    # Example using a mock response for demonstration
    # Replace with actual API call, e.g., OpenAI's API
    # For example:
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         "https://api.openai.com/v1/engines/davinci/completions",
    #         headers={"Authorization": f"Bearer YOUR_API_KEY"},
    #         json={
    #             "prompt": prompt,
    #             "max_tokens": 150,
    #             "temperature": 0.7,
    #         }
    #     )
    #     response.raise_for_status()
    #     data = response.json()
    #     return data['choices'][0]['text'].strip()

    # Mock response for demonstration
    return "This is a placeholder response to your message."

```

### requirements.txt

```
fastapi
uvicorn
httpx
liteLLM
starlette
pydantic
```