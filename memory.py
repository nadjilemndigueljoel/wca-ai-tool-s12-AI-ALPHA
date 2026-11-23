# Conversation memory and JSON management

import json
import os
from datetime import datetime


BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
SESSIONS_FOLDER = os.path.join(BASE_FOLDER, "sessions")
os.makedirs(SESSIONS_FOLDER, exist_ok=True)


def save_session(messages, summary):
    """Save a conversation and its summary to a timestamped JSON file."""
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filepath = os.path.join(SESSIONS_FOLDER, f"session_{date}.json")

    session_data = {
        "date": date,
        "messages": messages,
        "summary": summary,
    }

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(session_data, file, indent=4, ensure_ascii=False)

    return filepath


def load_session(filepath):
    """Load and return a previously saved session."""
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)