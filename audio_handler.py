"""
audio_handler.py

This module handles the extraction and transcription of audio from video files.
It uses moviepy for audio extraction and OpenAI's Whisper API for the
transcription of speech into text.
Key features:
- Extracting audio from video files
- Transcription of audio into text
- Management of temporary files
- Integration with OpenAI Whisper

"""

import os
from pathlib import Path
from moviepy.editor import VideoFileClip

class AudioHandler:
    def __init__(self, openai_client):
        self.openai_client = openai_client

    def extract_audio(self, video_path):
        """Extract audio from video file"""
        try:
            video = VideoFileClip(video_path)
            audio = video.audio
            temp_audio = f"temp_audio_{Path(video_path).stem}.wav"
            audio.write_audiofile(temp_audio)
            video.close()
            return temp_audio
        except Exception as e:
            print(f"Errore nell'estrazione dell'audio: {e}")
            return None

    def transcribe_audio(self, audio_path):
        """Convert audio to text using OpenAI Whisper"""
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                return transcript.text
        except Exception as e:
            print(f"Errore nella trascrizione dell'audio: {e}")
            return None
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
