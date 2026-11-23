# Clinic FAQ Assistant - Conversation and menu management

import json
import os

from assistant import get_ai_response
from memory import load_session, save_session
from prompts import SUMMARY_PROMPT


def validate_response(response):
    """Validate that an AI response is a usable clinic FAQ JSON object."""
    try:
        data = json.loads(response)
    except (json.JSONDecodeError, TypeError):
        return None

    if not isinstance(data, dict):
        return None

    required_fields = ("answer", "topic")
    if any(not data.get(field) for field in required_fields):
        return None

    return data


def validate_summary(response):
    """Validate that an AI response is a usable session summary."""
    try:
        data = json.loads(response)
    except (json.JSONDecodeError, TypeError):
        return None

    if not isinstance(data, dict):
        return None

    if not data.get("summary") or not isinstance(
        data.get("questions_and_answers"), list
    ):
        return None

    return data


def get_valid_response(messages, response_type="faq"):
    """Ask the AI and retry once when its JSON response is invalid."""
    for attempt in range(2):
        response = get_ai_response(
            messages,
            use_summary=(response_type == "summary"),
        )

        if response_type == "summary":
            data = validate_summary(response)
        else:
            data = validate_response(response)

        if data is not None:
            return data

        if attempt == 0:
            print("Invalid response. Trying again...")

    print("Sorry, I could not process the response.")
    return None


def start_session():
    """Start a conversation and save it when the patient exits."""
    messages = []

    print("\nWelcome to Clinic FAQ Assistant!")
    print("Ask your clinic questions. Type 'exit' to finish.")

    while True:
        question = input("\nYou: ").strip()

        if not question:
            print("Please enter a question.")
            continue

        if question.lower() == "exit":
            break

        messages.append({"role": "user", "content": question})

        result = get_valid_response(messages)
        if result is None:
            messages.pop()
            continue

        print("\nAssistant:", result["answer"])
        print("Topic:", result["topic"])

        follow_up = result.get("follow_up")
        if follow_up:
            print("Follow-up question:", follow_up)

        messages.append(
            {"role": "assistant", "content": json.dumps(result, ensure_ascii=False)}
        )

    if messages:
        summary_messages = messages + [
            {"role": "user", "content": SUMMARY_PROMPT}
        ]
        summary = get_valid_response(summary_messages, response_type="summary")

        if summary:
            filepath = save_session(messages, summary)
            print("\nSession saved:", filepath)


def open_past_session():
    filename = input("Enter the session file path: ").strip()

    try:
        if not os.path.exists(filename):
            filename = os.path.join("sessions", filename)

        session = load_session(filename)

        print("\nPrevious conversation:")

        for message in session["messages"]:
            print(f"{message['role']}:", message["content"])

        print("\nSummary:")
        print(json.dumps(session["summary"], indent=2, ensure_ascii=False))

    except FileNotFoundError:
        print("Session file not found.")
    except (json.JSONDecodeError, KeyError, OSError):
        print("Could not read this session file.")


def main():
    """Display the clinic assistant main menu."""
    while True:
        print("\n===== CLINIC FAQ ASSISTANT =====")
        print("1. Start a new session")
        print("2. Open a past session")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            start_session()
        elif choice == "2":
            open_past_session()
        elif choice == "3":
            print("Thank you for using Clinic FAQ Assistant.")
            break
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()