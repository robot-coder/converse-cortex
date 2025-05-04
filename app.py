from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import httpx
from typing import Optional, Dict, Any
import uvicorn

app = FastAPI(title="Web-based Chat Assistant")

# Placeholder for LLM interaction - replace with actual implementation or API calls
class LLMClient:
    def __init__(self):
        # Initialize with API keys or configs if needed
        pass

    async def generate_response(self, prompt: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a response from the LLM based on the prompt.
        """
        # For demonstration, echo the prompt; replace with actual LLM API call
        # Example: call to OpenAI API or other LLM providers
        try:
            # Simulate API call delay
            # response = await some_llm_api_call(prompt, conversation_id)
            response_text = f"Echo: {prompt}"
            return {"response": response_text}
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {str(e)}")

llm_client = LLMClient()

class Message(BaseModel):
    message: str
    conversation_id: Optional[str] = None

# Store conversations in-memory; for production, consider persistent storage
conversations: Dict[str, list] = {}

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    """
    Serve the front-end HTML page.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            #chat { border: 1px solid #ccc; padding: 10px; height: 400px; overflow-y: scroll; }
            #user-input { width: 80%; }
            #send-btn { width: 15%; }
        </style>
    </head>
    <body>
        <h1>Web-based Chat Assistant</h1>
        <div id="chat"></div>
        <input type="text" id="user-input" placeholder="Type your message..." />
        <button id="send-btn">Send</button>
        <script>
            const chatDiv = document.getElementById('chat');
            const inputBox = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');
            let conversationId = null;

            function appendMessage(sender, message) {
                const msgDiv = document.createElement('div');
                msgDiv.innerHTML = `<b>${sender}:</b> ${message}`;
                chatDiv.appendChild(msgDiv);
                chatDiv.scrollTop = chatDiv.scrollHeight;
            }

            sendBtn.onclick = async () => {
                const message = inputBox.value;
                if (!message) return;
                appendMessage('User', message);
                inputBox.value = '';

                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message, conversation_id: conversationId })
                });
                const data = await response.json();
                if (response.ok) {
                    appendMessage('Assistant', data.response);
                    conversationId = data.conversation_id;
                } else {
                    appendMessage('Error', data.detail || 'Failed to get response.');
                }
            };

            inputBox.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') sendBtn.click();
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/chat")
async def chat_endpoint(msg: Message):
    """
    Handle chat messages, maintain conversation context, and generate LLM responses.
    """
    try:
        conv_id = msg.conversation_id
        if conv_id and conv_id in conversations:
            conversation_history = conversations[conv_id]
        else:
            conv_id = str(len(conversations) + 1)
            conversation_history = []
            conversations[conv_id] = conversation_history

        # Append user message to history
        conversation_history.append({"role": "user", "content": msg.message})

        # Prepare prompt based on conversation history
        prompt = "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in conversation_history])

        # Generate response from LLM
        llm_response = await llm_client.generate_response(prompt, conversation_id=conv_id)
        reply = llm_response.get("response", "")

        # Append assistant response to history
        conversation_history.append({"role": "assistant", "content": reply})

        return {
            "response": reply,
            "conversation_id": conv_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: Run with uvicorn if executing directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)