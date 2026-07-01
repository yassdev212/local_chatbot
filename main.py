from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.responses import HTMLResponse

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str
    message: str


sessions = {}

@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    
    
    if request.session_id not in sessions:
        sessions[request.session_id] = []
        
    
    user_history = sessions[request.session_id]
    
   
    user_history.append({"role": "user", "content": request.message})
    
   
    ollama_payload = {
        "model": "llama3.2",
        "messages": user_history, 
        "stream": False
    }
    
    response = requests.post("http://localhost:11434/api/chat", json=ollama_payload)
    ai_text = response.json()["message"]["content"]
    
   
    user_history.append({"role": "assistant", "content": ai_text})
    
    return {"reply": ai_text}

@app.get("/")
def serve_homepage():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())