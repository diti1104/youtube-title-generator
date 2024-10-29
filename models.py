"""
models.py

 
This module manages the selection of AI models available for title generation.
It provides a user interface to select the desired model from several options
organized by provider (OpenAI, Anthropic, Meta-Llama).
Key features:
- Organization of AI models by provider
- Interactive selection interface
- Validation of user input

"""

class AIModels:
    def __init__(self):
        # Available models categorized by provider
        self.ai_models = {
            "OpenAI": ["gpt-4o", "gpt-4o-mini"],
            "Anthropic": ["claude-3.5-sonnet", "claude-3-haiku"],
            "Meta-Llama": ["llama-3.2"]
        }

    def select_model(self):
        """Allow user to select an AI model"""
        print("\nDisponibili modelli AI per categoria:")
        
        # Create a flat list of all models with their providers
        all_models = []
        for provider, models in self.ai_models.items():
            for model in models:
                all_models.append((provider, model))
        
        # Display models with sequential numbering
        current_provider = None
        for i, (provider, model) in enumerate(all_models, 1):
            if provider != current_provider:
                print(f"\n{provider}:")
                current_provider = provider
            print(f"  [{i}] {model}")
        
        while True:
            try:
                selection = input("\nSeleziona il numero del modello desiderato [1-{}]: ".format(len(all_models)))
                index = int(selection) - 1
                if 0 <= index < len(all_models):
                    provider, selected_model = all_models[index]
                    print(f"\nModello selezionato: {selected_model} ({provider})")
                    return selected_model
                else:
                    print(f"Selezione non valida. Inserisci un numero tra 1 e {len(all_models)}.")
            except ValueError:
                print("Per favore inserisci un numero valido.")
