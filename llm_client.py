import os
import json
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (e.g. OPENAI_API_KEY)
load_dotenv(override=True)

client = None
DEFAULT_MODEL = "gpt-4o-mini"

def init_client():
    global client, DEFAULT_MODEL
    # Reload environment variables
    load_dotenv(override=True)
    
    # Try getting key from environment first
    api_key = os.environ.get("OPENAI_API_KEY", "")
    
    # If not in environment, try Streamlit secrets
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("OPENAI_API_KEY", "")
        except Exception:
            pass
            
    if not api_key:
        client = None
        return

    try:
        if api_key.startswith("gsk_"):
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            DEFAULT_MODEL = "llama-3.1-8b-instant"
        else:
            client = OpenAI(api_key=api_key)
            DEFAULT_MODEL = "gpt-4o-mini"
    except Exception as e:
        client = None
        print(f"Error initializing LLM client: {e}")

def get_ai_recommendations(system_prompt: str, user_prompt: str, model: str = None) -> List[Dict[str, str]]:
    """
    Sends the constructed prompts to the AI API and parses the structured JSON response.
    Includes error handling to gracefully fallback if the API fails.
    """
    global client
    if client is None:
        init_client()
        
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
            
        data = json.loads(content)
        
        if "recommendations" in data and isinstance(data["recommendations"], list):
            return data["recommendations"]
        else:
            print("Unexpected JSON structure returned from LLM. Missing 'recommendations' key.")
            return []
            
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        # Reset client on failure to allow re-initialization on next attempt
        client = None
        return []
