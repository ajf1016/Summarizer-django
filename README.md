# Voice-to-Text Summarizer

This project is a voice-to-text summarizer that converts audio to text using Whisper ai and summarizes the text using Gemini LLM. The backend is built with Django and provides a REST API for integration.

## Table of Contents

- [Installation](#installation)
- [API Endpoints](#api-endpoints)

## Installation

To get a local copy up and running, follow these steps.

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- virtualenv (optional, but recommended)

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/ajf1016/Summarizer-django
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   cd coquus
   pip install -r requirements.txt
   python manage.py runserver

## API Endpoints
```markdown
POST api/v1/notes/upload-audio   DATA - audio_file : .mp3,.wav...
GET  convert-audio-to-text-and-summarize/audio-id
GET  get-all-notes/
GET  get-single-note/note-id/
GET  get-all-voices/
GET  get-single-voice/audio-id

