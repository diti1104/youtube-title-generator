import os
import whisper
from moviepy.editor import VideoFileClip

class AudioHandler:
    def __init__(self):
        self.model = whisper.load_model("base")  # Use "tiny" for faster but less accurate

    def extract_audio(self, video_path):
        audio_path = f"temp_audio_{os.path.basename(video_path)}.wav"
        try:
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path)
            return audio_path
        except Exception as e:
            print("❌ Error extracting audio:", e)
            return None

    def transcribe_audio(self, audio_path):
        try:
            print("📝 Transcribing with local Whisper...")
            result = self.model.transcribe(audio_path)
            text = result["text"]

            # Optional cleanup
            if os.path.exists(audio_path):
                os.remove(audio_path)

            return text
        except Exception as e:
            print("❌ Transcription error:", e)
            return None
