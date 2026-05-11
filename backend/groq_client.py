from groq import Groq
import os
from dotenv import load_dotenv
# แนะนำให้ดึงจาก Environment Variable แทนการเขียนตรงๆ
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
