from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent.llm import llm_runner

app = FastAPI()

# Allow frontend (Streamlit) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define message model
class Message(BaseModel):
    user_message: str

@app.post("/chat")
async def chat(msg: Message):
    # Simple rule-based response (replace with your own logic or LLM API)
    user_message = msg.user_message.lower()

    data = await llm_runner(user_message)
    
    return {"response":data}
