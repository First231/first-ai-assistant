from fastapi import FastAPI
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import SessionLocal, engine
from backend import models
from backend.groq_client import ask_llm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables
models.Base.metadata.create_all(bind=engine)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "AI server running"}


@app.post("/chat")
def chat(request: ChatRequest):

    db: Session = SessionLocal()

    ai_reply = ask_llm(request.message)

    chat = models.ChatHistory(
        user_message=request.message,
        ai_response=ai_reply
    )

    db.add(chat)
    db.commit()
    db.close()

    return {"response": ai_reply}


@app.get("/history")
def history():

    db: Session = SessionLocal()

    chats = db.query(models.ChatHistory).all()

    db.close()

    return chats
