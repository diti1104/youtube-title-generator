"""
language_manager.py

This module manages the application's multilingual support.
Loads language JSON files and provides access to localized strings.

Main features:
- Language file loading
- Language selection
- Localized string access
- Support for adding new languages
"""

import json
import os
from pathlib import Path

class LanguageManager:
    def __init__(self):
        self.current_language = 'en'  # Default to English
        self.strings = {}
        self.available_languages = self._get_available_languages()
        self.load_language('en')  # Load English by default

    def _get_available_languages(self):
        """Get list of available language files"""
        languages_dir = Path(__file__).parent / 'languages'
        language_files = languages_dir.glob('*.json')
        return {f.stem: f.stem.upper() for f in language_files}

    def select_language(self):
        """Let user select a language"""
        print("Select language:")
        for code, name in self.available_languages.items():
            print(f"[{code}] {name}")
        
        while True:
            choice = input("\nEnter language code: ").lower()
            if choice in self.available_languages:
                self.load_language(choice)
                return choice
            print("Invalid choice")

    def load_language(self, language_code):
        """Load language strings from JSON file"""
        try:
            language_file = Path(__file__).parent / 'languages' / f'{language_code}.json'
            with open(language_file, 'r', encoding='utf-8') as f:
                self.strings = json.load(f)
            self.current_language = language_code
        except FileNotFoundError:
            print(f"Language file not found: {language_code}")
            raise
        except json.JSONDecodeError:
            print(f"Error parsing language file: {language_code}")
            raise

    def get_string(self, key, *args):
        """Get localized string with optional formatting"""
        if not self.strings:
            raise ValueError("No language loaded")
        
        string = self.strings.get(key, f"Missing string: {key}")
        if args:
            return string.format(*args)
        return string

# Global instance
language_manager = LanguageManager()
