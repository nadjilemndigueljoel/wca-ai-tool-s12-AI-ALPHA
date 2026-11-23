# Clinic FAQ Assistant

## Project Description

Clinic FAQ Assistant is an AI-powered assistant designed to answer frequently asked questions about a small clinic.

It helps patients get information about:
- Clinic opening hours
- Medical services
- consultation prices
- Appointment booking

The assistant remember's the conversation history, refuses to provide medical diagnoses, and generates a summary at the end of each session.

## Project Team

Group Name: AI ALPHA

## Installation and setup

1. clone the repository.
2. Intall Python.
3. Intall the required packages:

...bash
pip install -r requirements.txt

4. Create a .env file in the project folder
5. Add your Gemini API key
GEMINI_API_KEY=your_api_key_here
6. Run the application:
python main.py

Security
The API key is stored in the .env file.
The .env file must never be uploaded to GitHub.

## How to use

When the application starts, the user has three options:

1. Start a new patient session.
2. Open a previous session.
3. Exit the application.

During a session, patints can ask questions.Type 'exit' to end the conversation.

The assistant then generates a summary and saves the session in the 'sessions' folder.

## sample conversation 

A sample conversation is available in the 'samples' folder.

## technologies used

- Python
- Google Gemini API
- Google-genai
- Python-dotenv
- JSON for conversation storage
- Git and GitHub for version control