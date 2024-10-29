# Video Title Generator

A powerful Python tool that automates the generation of SEO-optimized titles for social media videos using AI. This tool processes video clips by transcribing their audio content and generating engaging titles with relevant hashtags.

## Features

- 🎥 Process single videos or entire folders
- 🗣️ Automatic audio transcription using OpenAI Whisper
- 🤖 AI-powered title generation with multiple model options
- 🌐 Multi-language support
- #️⃣ Automatic hashtag generation and optimization
- 📏 Smart title length optimization for YouTube video (max 100 characters)
- 🔄 Batch processing capabilities

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- OpenRouter API key
- FFmpeg (for audio processing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/video-title-generator.git
cd video-title-generator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Usage

1. Run the main script:
```bash
python main.py
```

2. Select your preferred language (English or Italian)

3. Choose processing mode:
   - Single video processing
   - Folder batch processing

### Single Video Processing

```bash
1. Enter the video file path
2. Provide context description
3. Review generated title
4. Confirm to rename the file
```

### Batch Processing

```bash
1. Enter the folder path containing videos
2. Choose between:
   - Single context for all videos
   - Individual context for each video
3. Review generated titles
4. Confirm to rename all files
```

## Project Structure

```
video-title-generator/
├── languages/              # Language files
├── prompts/               # AI prompt templates
├── audio_handler.py       # Audio processing
├── file_handler.py        # File operations
├── language_manager.py    # Language management
├── models.py             # AI model selection
├── prompt_handler.py     # Title generation
└── main.py  # Main script
```

## Adding New Languages

1. Create a new language file in `languages/` (e.g., `fr.json`)
2. Add corresponding prompt template in `prompts/` (e.g., `title_generation_prompt_fr.txt`)
3. The system will automatically detect and include the new language

## Available AI Models

- OpenAI:
  - gpt-4o
  - gpt-4o-mini
- Anthropic:
  - claude-3.5-sonnet
  - claude-3-haiku
- Meta-Llama:
  - llama-3.2

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for Whisper API
- OpenRouter for AI model access
- MoviePy for video processing

## Author

Jacopo Luca Maria Latrofa
- GitHub: [@fralapo](https://github.com/fralapo)
