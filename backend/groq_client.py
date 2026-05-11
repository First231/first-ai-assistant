import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv() # โหลดค่าจาก .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def def ask_llm(prompt):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            # เพิ่มบรรทัดนี้เพื่อกำหนดหน้าที่ให้ AI
            {"role": "system", "content": "You are a helpful assistant. Provide detailed answers in Thai and do not repeat the user's input."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content
