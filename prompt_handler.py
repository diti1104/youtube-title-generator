# Prompt handling and title generation module
# Manages prompt templates and API interactions for title generation

import requests
import os
from pathlib import Path
from language_manager import language_manager as lm

def load_prompt_template(language_code):
    """Load the prompt template from file based on language"""
    prompt_path = Path(__file__).parent / 'prompts' / f'title_generation_prompt_{language_code}.txt'
    try:
        with open(prompt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(lm.get_string("prompt_file_not_found", str(prompt_path)))
        print(lm.get_string("check_prompt_file"))
        raise

def optimize_title_length(title, max_length=100):
    """Optimize title length while preserving essential information"""
    if len(title) <= max_length:
        return title
        
    # Split into title and hashtags
    parts = title.split('#')
    main_title = parts[0].strip()
    hashtags = ['#' + tag.strip() for tag in parts[1:] if tag.strip()]
    
    # If we have more than 3 hashtags, keep only the 3 most relevant ones
    if len(hashtags) > 3:
        hashtags = hashtags[:3]
    
    # Calculate available space for main title
    hashtags_str = ' ' + ' '.join(hashtags)
    available_title_length = max_length - len(hashtags_str)
    
    if available_title_length < 20:  # Minimum reasonable title length
        # Reduce hashtags if title space is too small
        while len(hashtags) > 1 and available_title_length < 20:
            hashtags.pop()
            hashtags_str = ' ' + ' '.join(hashtags)
            available_title_length = max_length - len(hashtags_str)
    
    # Shorten main title if needed
    if len(main_title) > available_title_length:
        words = main_title.split()
        shortened_title = []
        current_length = 0
        
        # Keep adding words until we reach the limit
        for word in words:
            if current_length + len(word) + 1 <= available_title_length:
                shortened_title.append(word)
                current_length += len(word) + 1
            else:
                break
        
        main_title = ' '.join(shortened_title)
    
    # Combine title and hashtags
    return f"{main_title}{hashtags_str}"

def generate_title(openrouter_api_key, selected_model, transcription, context, language_code):
    """Generate title using selected AI model through OpenRouter"""
    try:
        # Load prompt template for selected language
        prompt_template = load_prompt_template(language_code)
        
        # Format prompt with context and transcription
        prompt = prompt_template.format(
            context=context,
            transcription=transcription
        )

        headers = {
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/video-title-generator",
            "X-Title": "Video Title Generator"
        }

        data = {
            "model": selected_model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional social media title generator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        title = response.json()['choices'][0]['message']['content'].strip()
        
        # Ensure title meets character limit
        optimized_title = optimize_title_length(title)
        
        # Verify the final length
        if len(optimized_title) > 100:
            print(lm.get_string("title_too_long", len(optimized_title)))
            optimized_title = optimize_title_length(optimized_title, 100)
        
        return optimized_title
        
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if hasattr(e.response, 'json'):
            try:
                error_data = e.response.json()
                if 'error' in error_data:
                    error_msg = f"{error_data['error'].get('message', str(e))}"
            except:
                pass
        print(lm.get_string("title_generation_error", error_msg))
        return None
    except Exception as e:
        print(lm.get_string("title_generation_error", str(e)))
        return None
