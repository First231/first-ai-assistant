from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

# นำเข้าส่วนประกอบจากไฟล์อื่นๆ ในโปรเจกต์
from backend.database import SessionLocal, engine
from backend import models
from backend.groq_client import ask_llm
from fastapi.middleware.cors import CORSMiddleware

# สร้างฐานข้อมูลและตารางอัตโนมัติ (ถ้ายังไม่มี)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ตั้งค่า CORS เพื่อให้หน้าเว็บ (GitHub Pages) คุยกับ Server (Render) ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ฟังก์ชันสำหรับจัดการ Database Session (เปิด-ปิดอัตโนมัติ)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# กำหนดรูปแบบข้อมูลที่รับมาจากหน้าเว็บ
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "AI server is running safely!"}

@app.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # 1. ส่งข้อความไปถาม AI ผ่าน Groq
        ai_reply = ask_llm(request.message)

        # 2. บันทึกประวัติการสนทนาลงใน SQLite
        new_chat = models.ChatHistory(
            user_message=request.message,
            ai_response=ai_reply
        )
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        
        # 3. ส่งคำตอบกลับไปที่หน้าเว็บ
        return {"response": ai_reply}
        
    except Exception as e:
        # ถ้ามีข้อผิดพลาด (เช่น API Key ผิด) จะแจ้งเตือนกลับไป
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="AI Service Error. Please check logs.")

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    # ดึงประวัติการแชททั้งหมดออกมาดู
    chats = db.query(models.ChatHistory).all()
    return chats
