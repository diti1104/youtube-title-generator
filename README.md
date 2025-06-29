# YouTube Video Title Generator

This project is a powerful AI-based tool that helps content creators **automatically generate optimized and engaging YouTube video titles**. It extracts audio from a video, transcribes it using OpenAI's Whisper model, and then analyzes the content using large language models via OpenRouter (e.g., `mistralai/mistral-7b-instruct`) to generate titles based on the video content and user-provided context.

---

## Features

- Automatic audio extraction from video
- Accurate transcription using Whisper
- AI-powered title generation using OpenRouter (Mistral, Gemma, etc.)
- Multilingual UI support via `languages/` folder
- Batch folder processing support
- Optional video file renaming with generated title
- Easy-to-extend architecture

---

## Project Structure


---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/diti1104/youtube-title-generator.git
cd youtube-title-generator
python -m venv venv
venv\Scripts\activate    # On Windows
# or
source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
OPENROUTER_API_KEY=your_openrouter_api_key
MODEL=mistralai/mistral-7b-instruct
OPENAI_API_KEY=dummy
