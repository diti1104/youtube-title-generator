import requests
import json

def generate_title(api_key, model, transcript, context, language_code):
    try:
        system_prompt = f"You are a helpful assistant. Generate a YouTube title in {language_code} based on transcript and context."
        user_prompt = f"Transcript: \n{transcript}\n\nContext:\n{context}"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print("❌ OpenRouter API error:", response.status_code, response.text)
            return None

    except Exception as e:
        print("❌ Error generating title:", e)
        return None
