import json
from typing import List, Dict, Any

def build_system_prompt() -> str:
    return """You are an expert AI food critic and restaurant recommender.
Your task is to analyze a list of pre-filtered restaurants and select the top options (up to 3) that best match the user's specific nuance or occasion.

You MUST output your response STRICTLY as a valid JSON object. Do not include markdown code blocks (like ```json) or any conversational text.
The JSON object must have a single key "recommendations" containing an array of objects.
Each object in the array must have exactly two keys:
1. "name": The exact name of the restaurant from the provided list.
2. "reason": A personalized, persuasive 1-2 sentence explanation of WHY this restaurant is a great fit for the user's specific nuance, referencing the data provided.

Example Output:
{
  "recommendations": [
    {
      "name": "Pasta Fresca",
      "reason": "With its dim lighting and live acoustic music, it provides the perfect intimate setting for your romantic anniversary dinner."
    }
  ]
}"""

def build_user_prompt(nuance: str, restaurants: List[Dict[str, Any]]) -> str:
    # Filter out empty or irrelevant keys to save tokens
    clean_restaurants = []
    for r in restaurants:
        clean_restaurants.append({
            "name": r.get("name"),
            "location": r.get("location"),
            "cuisine": r.get("cuisine"),
            "rating": r.get("rating"),
            "cost": r.get("cost")
        })
        
    restaurants_context = json.dumps(clean_restaurants, indent=2)
    
    # If the user didn't provide a specific nuance, provide a generic one.
    if not nuance or nuance.strip() == "":
        nuance = "I am just looking for the overall best and most popular options from this list."
    
    return f"""User's Specific Request / Nuance: "{nuance}"

Here are the pre-filtered restaurants available (in JSON format):
{restaurants_context}

Based on the user's request, select and rank the best options (up to 3) from the list above. Output ONLY a valid JSON object."""
