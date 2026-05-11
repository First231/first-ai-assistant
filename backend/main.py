from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from backend.database import SessionLocal, engine
from backend import models
from backend.groq_client import ask_llm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# สร้าง Table อัตโนมัติ
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ฟังก์ชันช่วยจัดการ Database Session แบบปลอดภัย
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "AI server running"}

@app.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # เรียกใช้ AI
        ai_reply = ask_llm(request.message)

        # บันทึกลง Database
        new_chat = models.ChatHistory(
            user_message=request.message,
            ai_response=ai_reply
        )
        db.add(new_chat)
        db.commit()
        
        return {"response": ai_reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def history(db: Session = Depends(get_db)):
    # ดึงข้อมูลทั้งหมด
    return db.query(models.ChatHistory).all()
