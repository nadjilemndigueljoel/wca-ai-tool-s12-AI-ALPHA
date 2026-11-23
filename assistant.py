# Clinic FAQ Assistant - Gemini API connection

from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from prompts import SUMMARY_PROMPT, SYSTEM_PROMPT


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")


client = genai.Client(api_key=GEMINI_API_KEY)


def get_ai_response(messages, use_summary=False):
    """Send conversation history to Gemini and return the response text."""
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    contents = [
        {
            "role": "user" if message["role"] == "user" else "model",
            "parts": [{"text": message["content"]}],
        }
        for message in messages
    ]

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=(
                    SUMMARY_PROMPT if use_summary else SYSTEM_PROMPT
                ),
                response_mime_type="application/json",
            ),
        )
        return response.text
    except Exception as error:
        print("API error:", error)
        return None