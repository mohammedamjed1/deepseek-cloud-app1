from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
import os

app = FastAPI()

# السماح بالوصول من أي دومين
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ربط مجلد public للملفات الثابتة (HTML, JS, CSS)
app.mount("/", StaticFiles(directory="public", html=True), name="static")

# مفتاح API من DeepSeek (تم تعيينه كـ Environment Variable)
DEEPSEEK_API_KEY = os.environ.get("deepseek1")
DEEPSEEK_URL = "https://api.deepseek.ai/v1/generate"

@app.post("/ask")
async def ask(question: str = Form(...)):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"prompt": question, "max_tokens": 500}

    try:
        response = requests.post(DEEPSEEK_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {"answer": data.get("output_text", "لم يتم الحصول على إجابة")}
    except Exception as e:
        return {"answer": f"حدث خطأ: {str(e)}"}
