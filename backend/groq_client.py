import os
from dotenv import load_dotenv
from groq import Groq

# โหลดค่าจากไฟล์ .env (ถ้ามี) สำหรับรันในเครื่องตัวเอง
load_dotenv() 

# os.getenv จะไปดึงค่าจากไฟล์ .env (ตอนรันในคอม) 
# หรือดึงจากหน้า Settings ของ Render (ตอนออนไลน์) มาให้เองโดยอัตโนมัติ
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)
def ask_llm(prompt):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            # ใส่บทบาทให้ AI เพื่อให้เลิกตอบทวนคำพูดเรา
            {"role": "system", "content": "You are a helpful assistant. Answer clearly in Thai."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content
