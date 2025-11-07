from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DEEPSEEK_API_KEY = os.environ.get("deepseek1")
DEEPSEEK_API_URL = "https://api.deepseek.ai/v1/generate"

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")
    
    if not question:
        return {"error": "No question provided."}

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": question
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return {"answer": result.get("output_text", "لا يوجد إجابة")}
    except Exception as e:
        return {"error": f"حدث خطأ في معالجة السؤال: {str(e)}"}
