from groq import Groq
import os

# แนะนำให้ดึงจาก Environment Variable แทนการเขียนตรงๆ
client = Groq(api_key="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")

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
