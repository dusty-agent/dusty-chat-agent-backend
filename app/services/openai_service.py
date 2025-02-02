import openai
from app.core.config import config

openai.api_key = config.OPENAI_API_KEY

def chat_with_gpt(user_message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"OpenAI API 호출 실패: {e}"
