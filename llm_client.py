import os
import json
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (e.g. OPENAI_API_KEY)
load_dotenv()

try:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if api_key.startswith("gsk_"):
        # The user provided a Groq API key, use Groq's OpenAI-compatible endpoint!
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        DEFAULT_MODEL = "llama-3.1-8b-instant"
    else:
        # Standard OpenAI initialization
        client = OpenAI(api_key=api_key)
        DEFAULT_MODEL = "gpt-4o-mini"
except Exception as e:
    client = None
    DEFAULT_MODEL = "gpt-4o-mini"
    print(f"Warning: OPENAI_API_KEY not found or invalid ({e}). AI recommendations will be disabled, and the app will fallback to deterministic filters.")

def get_ai_recommendations(system_prompt: str, user_prompt: str, model: str = None) -> List[Dict[str, str]]:
    """
    Sends the constructed prompts to the AI API and parses the structured JSON response.
    Includes error handling to gracefully fallback if the API fails.
    """
    if not client:
        return []
        
    if not model:
        model = DEFAULT_MODEL
        
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        if not content:
            print("Received empty response from LLM.")
            return []
            
        # Parse the JSON string into a Python dictionary
        data = json.loads(content)
        
        if "recommendations" in data and isinstance(data["recommendations"], list):
            return data["recommendations"]
        else:
            print("Unexpected JSON structure returned from LLM. Missing 'recommendations' key.")
            return []
            
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        return []
