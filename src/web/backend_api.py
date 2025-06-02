from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent.llm import llm_runner

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    user_message: str

@app.post("/chat")
async def chat(msg: Message):
    user_message = msg.user_message.lower()

    data = await llm_runner(user_message)
    
    return {"response":data}
