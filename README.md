# VoiceNotes - Full Stack Speech Recognition App

Frontend: HTML/CSS/JS (Web Speech API for speech-to-text and text-to-speech)
Backend: Python Flask REST API
Database: SQLite (created automatically as transcripts.db)

## Run it in VS Code
1. Open this folder in VS Code
2. Open a terminal and run:
   python -m venv venv
   venv\Scripts\activate        (Windows)   |   source venv/bin/activate  (Mac/Linux)
   pip install -r requirements.txt
   python app.py
3. Open http://127.0.0.1:5000 in Chrome or Edge and allow the microphone.

## API
GET    /api/transcripts        list saved notes
POST   /api/transcripts        save a note  {"text": "...", "language": "en-US"}
DELETE /api/transcripts/<id>   delete a note
GET    /api/export             download all notes as .txt

## Notes
- Speech recognition works in Chrome and Edge (Firefox does not support it).
- It needs an internet connection because the browser sends audio to its speech service.
