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
        self.current_language = 'en'
        self.strings = {}
        self.available_languages = self._get_available_languages()

        if 'en' not in self.available_languages:
            print("❌ English language file (en.json) is required.")
            raise FileNotFoundError("en.json not found in languages directory")

        self.load_language('en')  # Default to English

    def _get_available_languages(self):
        """Get list of available language files"""
        languages_dir = Path(__file__).parent / 'languages'
        if not languages_dir.exists():
            print("❌ 'languages' folder not found.")
            raise FileNotFoundError("'languages' directory is missing")

        language_files = languages_dir.glob('*.json')
        return {
            f.stem: f.stem.upper()
            for f in language_files
            if f.is_file() and f.suffix == ".json"
        }

    def select_language(self):
        """Prompt user to choose a language"""
        print("\n🌍 Available Languages:")
        for code, name in self.available_languages.items():
            print(f"[{code}] {name}")

        while True:
            choice = input("\n🔤 Enter language code (e.g. en, hi): ").lower()
            if choice in self.available_languages:
                self.load_language(choice)
                return choice
            print("❌ Invalid code. Try again.")

    def load_language(self, language_code):
        """Load language file by code"""
        try:
            language_file = Path(__file__).parent / 'languages' / f'{language_code}.json'
            with open(language_file, 'r', encoding='utf-8') as f:
                self.strings = json.load(f)
            self.current_language = language_code
        except FileNotFoundError:
            print(f"❌ Language file not found: {language_code}.json")
            raise
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {language_code}.json")
            raise

    def get_string(self, key, *args):
        """Get localized string, optionally formatted"""
        if not self.strings:
            raise ValueError("No language loaded")

        string = self.strings.get(key, f"⚠️ Missing string: {key}")
        return string.format(*args) if args else string


# Global instance
language_manager = LanguageManager()
