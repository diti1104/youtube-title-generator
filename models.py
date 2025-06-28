import os
from dotenv import load_dotenv

load_dotenv()

class AIModels:
    def __init__(self):
        # ✅ Use correct model names from https://openrouter.ai/models
        self.available_models = [
            "mistralai/mistral-7b-instruct",
            "google/gemma-7b-it",
            "meta-llama/llama-3-8b-instruct",      # Optional, fast & good
            "openai/gpt-3.5-turbo"                  # Optional, needs access
        ]

    def select_model(self):
        # ✅ Check if the model is defined in the .env file
        env_model = os.getenv("MODEL")
        if env_model:
            if env_model in self.available_models:
                print(f"✅ Using model from .env: {env_model}")
                return env_model
            else:
                print(f"⚠️ MODEL in .env not recognized: {env_model}. Using manual selection...")

        # ✅ Ask user to choose from available list
        print("\nAvailable OpenRouter Models:")
        for i, model in enumerate(self.available_models, 1):
            print(f"{i}. {model}")

        choice = input("Choose model number (default 1): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(self.available_models):
            return self.available_models[int(choice) - 1]
        
        # Default fallback model
        return self.available_models[0]
