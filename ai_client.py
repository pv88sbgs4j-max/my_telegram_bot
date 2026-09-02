import os
from openai import OpenAI
from config import DEEPSEEK_API_KEY

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def ask_deepseek(promt: str):
    try:
        response = client.chat.completions.create(
            model = "deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "Ты — полезный футбольный ассистент. Отвечай кратко и по делу."},
                {"role": "user", "content": promt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content 
    except Exception as e:
        return f"❌ Ошибка при запросе к DeepSeek: {e}"

