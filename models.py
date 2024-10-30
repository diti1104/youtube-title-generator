# Models configuration and selection module
# Manages available AI models and user selection

class AIModels:
    def __init__(self):
        # Available models categorized by provider with their OpenRouter identifiers
        self.ai_models = {
            "OpenAI": [
                "openai/gpt-4o",
                "openai/gpt-4o-mini"
            ],
            "Anthropic": [
                "anthropic/claude-3.5-sonnet"
            ],
            "Google": [
                "google/gemini-flash-1.5-8b"
            ],
            "Meta": [
                "meta-llama/llama-3.2-11b-vision-instruct:free"
            ]
        }

    def select_model(self):
        """Allow user to select an AI model"""
        print("\nDisponibili modelli AI per categoria:")
        
        # Create a list of tuples (provider, model) for continuous numbering
        all_models_with_providers = []
        for provider, models in self.ai_models.items():
            for model in models:
                all_models_with_providers.append((provider, model))
        
        # Display models with continuous numbering
        current_provider = None
        for i, (provider, model) in enumerate(all_models_with_providers, 1):
            if provider != current_provider:
                print(f"\n{provider}:")
                current_provider = provider
            # Extract just the model name without provider prefix for cleaner display
            model_name = model.split('/')[-1]
            print(f"  [{i}] {model_name}")
        
        while True:
            try:
                selection = input(f"\nSeleziona il numero del modello [1-{len(all_models_with_providers)}]: ")
                index = int(selection) - 1
                if 0 <= index < len(all_models_with_providers):
                    provider, selected_model = all_models_with_providers[index]
                    # Extract model name without provider prefix for display
                    model_name = selected_model.split('/')[-1]
                    print(f"\nModello selezionato: {model_name} ({provider})")
                    return selected_model
                else:
                    print(f"Selezione non valida. Inserisci un numero tra 1 e {len(all_models_with_providers)}.")
            except ValueError:
                print("Per favore inserisci un numero valido.")
