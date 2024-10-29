"""
file_handler.py

 
This module handles all file operations, including sanitization of filenames
and handling of renaming operations. It is responsible for ensuring that file names are
compatible with the operating system and handles file system operations in a secure manner.
Main features:
- File name sanitization (removal of invalid characters)
- Secure renaming of video files
- Searching for video files in a directory
- Management of supported video extensions

"""

import os
from pathlib import Path
import re

def sanitize_filename(filename):
    """Sanitize filename by removing invalid characters"""
    # Remove quotes and parentheses
    filename = filename.replace('"', '').replace('(', '').replace(')', '')
    
    # Replace invalid characters with underscores
    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, '_', filename)
    
    # Remove multiple consecutive underscores
    filename = re.sub(r'_+', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    return filename

def rename_video(old_path, new_title):
    """Rename video file with new title"""
    try:
        path = Path(old_path)
        sanitized_title = sanitize_filename(new_title)
        new_filename = f"{sanitized_title}{path.suffix}"
        new_path = path.parent / new_filename
        os.rename(old_path, new_path)
        return True
    except Exception as e:
        print(f"Errore nel rinominare il file: {e}")
        return False

def get_video_files(folder_path):
    """Get list of video files in a folder"""
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv'}
    return [
        file for file in os.listdir(folder_path)
        if Path(file).suffix.lower() in video_extensions
    ]
