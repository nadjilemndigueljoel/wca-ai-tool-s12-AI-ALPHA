# Load environment variables
import os

from dotenv import load_dotenv

load_dotenv()

# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")