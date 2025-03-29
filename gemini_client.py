import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY is missing. Please add it to .env")

genai.configure(api_key=api_key)

def get_gemini_model():
    return genai.GenerativeModel("gemini-1.5-pro-002")

def get_gemini_chat():
    model = get_gemini_model()
    return model.start_chat(history=[
        {
            "role": "user",
            "parts": [
                "You're an expert AI strategist in waste management and energy policy. "
                "Use data and policy context to offer layered, data-driven recommendations."
            ]
        },
        {
            "role": "model",
            "parts": [
                "Understood. I’ll focus on policy suggestions, energy forecasting, and regional best practices."
            ]
        }
    ])