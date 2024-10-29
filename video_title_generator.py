"""
video_title_generator.py

Main script that orchestrates the video title generation process.
Coordinates interaction between various modules to handle the entire workflow,
from audio extraction to final title generation.

Main features:
- Complete workflow management
- Main user interface
- Module coordination
- API key management
- Single and batch video processing
- Error handling and user feedback
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

from models import AIModels
from file_handler import rename_video, get_video_files
from audio_handler import AudioHandler
from prompt_handler import generate_title
from language_manager import language_manager as lm

class VideoTitleGenerator:
    def __init__(self):
        load_dotenv()
        
        # Select language (starts with English interface, then switches to selected language)
        self.language_code = lm.select_language()
        
        # From here on, all strings will be in the selected language
        
        # Check for required API keys
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        
        if not self.openai_api_key:
            print(lm.get_string("api_key_missing", "OPENAI_API_KEY"))
            print(lm.get_string("api_key_instructions", "create a .env file", "OpenAI"))
            raise ValueError("OPENAI_API_KEY missing")
            
        if not self.openrouter_api_key:
            print(lm.get_string("api_key_missing", "OPENROUTER_API_KEY"))
            print(lm.get_string("api_key_instructions", "add to the .env file", "OpenRouter"))
            raise ValueError("OPENROUTER_API_KEY missing")
        
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        self.audio_handler = AudioHandler(self.openai_client)
        self.models = AIModels()
        self.selected_model = None

    def process_video(self, video_path, context):
        """Process a single video file"""
        print(lm.get_string("processing_video", video_path))
        
        # Extract and transcribe audio
        audio_path = self.audio_handler.extract_audio(video_path)
        if not audio_path:
            return None
        
        transcription = self.audio_handler.transcribe_audio(audio_path)
        if not transcription:
            return None
        
        print(lm.get_string("transcription_for", Path(video_path).name))
        print(transcription)
        
        # Select model if not already selected
        if not self.selected_model:
            self.selected_model = self.models.select_model()
        
        # Generate title
        title = generate_title(
            self.openrouter_api_key,
            self.selected_model,
            transcription,
            context,
            self.language_code
        )
        if not title:
            return None
        
        return title

    def process_folder(self, folder_path, shared_context=None):
        """Process all videos in a folder"""
        results = []
        
        # Get list of video files
        video_files = get_video_files(folder_path)
        
        for file in video_files:
            video_path = os.path.join(folder_path, file)
            print(lm.get_string("processing_video", file))
            
            # Use shared context if provided, otherwise ask for individual context
            context = shared_context if shared_context is not None else input(lm.get_string("enter_context_for", file))
            result = self.process_video(video_path, context)
            
            if result:
                results.append((video_path, result))
        
        return results

def main():
    try:
        generator = VideoTitleGenerator()
        
        print(lm.get_string("welcome"))
        choice = input(lm.get_string("select_process"))
        
        if choice == "1":
            video_path = input(lm.get_string("enter_video_path"))
            if not os.path.exists(video_path):
                print(lm.get_string("video_not_found"))
                return
                
            context = input(lm.get_string("enter_context"))
            
            # Process video and generate title
            title = generator.process_video(video_path, context)
            if not title:
                print(lm.get_string("title_generation_error", ""))
                return
                
            # Preview title
            print(lm.get_string("title_generated"))
            print(title)
            
            # Confirm and rename
            confirm = input(lm.get_string("rename_confirm"))
            if confirm.lower() in ['s', 'y']:
                if rename_video(video_path, title):
                    print(lm.get_string("rename_success"))
                else:
                    print(lm.get_string("rename_error"))
        
        elif choice == "2":
            folder_path = input(lm.get_string("enter_folder_path"))
            if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
                print(lm.get_string("folder_not_found"))
                return
            
            # Ask for context preference
            context_choice = input(lm.get_string("use_same_context"))
            shared_context = None
            if context_choice.lower() in ['s', 'y']:
                shared_context = input(lm.get_string("enter_shared_context"))
                
            results = generator.process_folder(folder_path, shared_context)
            
            if not results:
                print(lm.get_string("no_videos_processed"))
                return
                
            print(lm.get_string("generated_titles_summary"))
            for video_path, title in results:
                print(f"\n{lm.get_string('processing_video', Path(video_path).name)}")
                print(title)
            
            confirm = input(lm.get_string("rename_all_confirm"))
            if confirm.lower() in ['s', 'y']:
                for video_path, title in results:
                    if rename_video(video_path, title):
                        print(lm.get_string("rename_multiple_success", Path(video_path).name))
                    else:
                        print(lm.get_string("rename_multiple_error", Path(video_path).name))
        
        else:
            print(lm.get_string("invalid_choice"))
            
    except ValueError as e:
        # API key errors are already handled with custom messages
        pass
    except Exception as e:
        print(lm.get_string("unexpected_error", str(e)))

if __name__ == "__main__":
    main()
