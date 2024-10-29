# File operations module
# Handles file system operations, name sanitization, and video file management

import os
from pathlib import Path
import re

def sanitize_filename(filename):
    # Keep alphanumeric, spaces, hashtags, apostrophes, and accented characters
    # Includes: àáâãäåèéêëìíîïòóôõöùúûüýÿñ
    sanitized = re.sub(r'[^a-zA-Z0-9\s\'#àáâãäåèéêëìíîïòóôõöùúûüýÿñÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÝŸÑ]', '', filename)
    
    # Remove multiple consecutive spaces
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Remove leading/trailing spaces
    sanitized = sanitized.strip()
    
    # Ensure the filename is not empty
    if not sanitized:
        sanitized = "untitled"
    
    return sanitized

def rename_video(old_path, new_title):
    # Rename video file with new title
    try:
        path = Path(old_path)
        sanitized_title = sanitize_filename(new_title)
        new_filename = f"{sanitized_title}{path.suffix}"
        new_path = path.parent / new_filename
        os.rename(old_path, new_path)
        return True
    except Exception as e:
        print(f"Error renaming file: {e}")
        return False

def get_video_files(folder_path):
    # Get list of video files in a folder
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv'}
    return [
        file for file in os.listdir(folder_path)
        if Path(file).suffix.lower() in video_extensions
    ]
