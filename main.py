# Main script for video title generation
# Orchestrates the entire process from video processing to title generation

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
        
        # Check for required API keys
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        
        # Verify OpenAI API key
        if not self.openai_api_key:
            key_name = "OPENAI_API_KEY"
            print(f"{key_name} {lm.get_string('api_key_missing')}")
            print(f"{lm.get_string('create_env_file')} {key_name}")
            raise ValueError(f"{key_name} missing")
            
        # Verify OpenRouter API key
        if not self.openrouter_api_key:
            key_name = "OPENROUTER_API_KEY"
            print(f"{key_name} {lm.get_string('api_key_missing')}")
            print(f"{lm.get_string('add_to_env_file')} {key_name}")
            raise ValueError(f"{key_name} missing")
        
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        self.audio_handler = AudioHandler(self.openai_client)
        self.models = AIModels()
        self.selected_model = None

    def process_video(self, video_path, context):
        # Process a single video file
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
        return title

    def process_folder(self, folder_path, shared_context=None):
        # Process all videos in a folder
        results = []
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

def get_path(input_message, is_folder=False):
    # Function to get and verify the existence of a file or folder path
    path = input(lm.get_string(input_message))
    if not os.path.exists(path) or (is_folder and not os.path.isdir(path)):
        print(lm.get_string("folder_not_found" if is_folder else "video_not_found"))
        return None
    return path

def confirm_action(message_key):
    # Function to confirm user's action
    confirm = input(lm.get_string(message_key))
    return confirm.lower() in ['s', 'y']

def process_and_rename(generator, video_path, context):
    # Function to process a video and rename it with the generated title
    title = generator.process_video(video_path, context)
    if not title:
        print(lm.get_string("title_generation_error", ""))
        return False

    print(lm.get_string("title_generated"))
    print(title)

    if confirm_action("rename_confirm"):
        if rename_video(video_path, title):
            print(lm.get_string("rename_success"))
            return True
        else:
            print(lm.get_string("rename_error"))
    return False

def main():
    try:
        generator = VideoTitleGenerator()
        
        print(lm.get_string("welcome"))
        choice = input(lm.get_string("select_process"))
        
        if choice == "1":
            # Case 1: Single video processing
            # Steps:
            # 1. Get video path
            # 2. Get context description
            # 3. Process video and generate title
            # 4. Confirm and rename if successful
            video_path = get_path("enter_video_path")
            if video_path:
                context = input(lm.get_string("enter_context"))
                process_and_rename(generator, video_path, context)

        elif choice == "2":
            # Case 2: Batch processing of multiple videos
            # Steps:
            # 1. Get folder path
            # 2. Ask for shared/individual context preference
            # 3. Process all videos in folder
            # 4. Show summary of generated titles
            # 5. Confirm and rename all if successful
            folder_path = get_path("enter_folder_path", is_folder=True)
            if folder_path:
                shared_context = input(lm.get_string("enter_shared_context")) if confirm_action("use_same_context") else None
                results = generator.process_folder(folder_path, shared_context)

                if not results:
                    print(lm.get_string("no_videos_processed"))
                else:
                    print(lm.get_string("generated_titles_summary"))
                    for video_path, title in results:
                        print(f"\n{lm.get_string('processing_video', Path(video_path).name)}")
                        print(title)

                    if confirm_action("rename_all_confirm"):
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
