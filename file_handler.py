# file_handler.py
# Handles file system operations, name sanitization, and video file management

import os
from pathlib import Path
import re

def sanitize_filename(filename):
    # Allow alphanumeric, spaces, hashtags, apostrophes, and accented characters
    sanitized = re.sub(
        r"[^a-zA-Z0-9\s\'#àáâãäåèéêëìíîïòóôõöùúûüýÿñÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÝŸÑ]",
        "",
        filename,
    )
    sanitized = re.sub(r"\s+", " ", sanitized).strip()

    return sanitized or "untitled"

def rename_video(old_path, new_title):
    try:
        path = Path(old_path)
        sanitized_title = sanitize_filename(new_title)
        new_filename = f"{sanitized_title}{path.suffix}"
        new_path = path.parent / new_filename

        if new_path.exists():
            print(f"⚠️ File with name {new_filename} already exists. Skipping rename.")
            return False

        os.rename(path, new_path)
        return True
    except Exception as e:
        print(f"❌ Error renaming file: {e}")
        return False

def get_video_files(folder_path):
    video_extensions = {".mp4", ".avi", ".mov", ".mkv"}

    try:
        return [
            file for file in os.listdir(folder_path)
            if Path(file).suffix.lower() in video_extensions and os.path.isfile(os.path.join(folder_path, file))
        ]
    except Exception as e:
        print(f"❌ Error listing video files: {e}")
        return []
