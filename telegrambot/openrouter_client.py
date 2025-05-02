import requests
# from telegrambot.openrouter_client import generate_openrouter_response
from blog.models import Blog

API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct"  # You can change to openchat, zephyr, etc.

def generate_openrouter_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": ["https://tbsassistant.onrender.com", "https://127.0.0.1"],  # Optional
        "X-Title": "MyTelegramBot"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error talking to AI: {str(e)}"


