import unittest
from prompt_builder import build_user_prompt

class TestPromptBuilder(unittest.TestCase):
    def test_build_user_prompt(self):
        restaurants = [
            {
                "name": "Rest A", 
                "location": "City", 
                "cuisine": "Food", 
                "rating": 4.5, 
                "cost": 100, 
                "extra_key_to_ignore": "ignore"
            }
        ]
        nuance = "I want something nice."
        
        prompt = build_user_prompt(nuance, restaurants)
        
        # Check if nuance is in prompt
        self.assertIn("I want something nice.", prompt)
        
        # Check if restaurant name is in prompt
        self.assertIn("Rest A", prompt)
        
        # Check if extra key is filtered out to save tokens
        self.assertNotIn("extra_key_to_ignore", prompt)
        
    def test_empty_nuance_fallback(self):
        prompt = build_user_prompt("", [{"name": "Rest A"}])
        self.assertIn("I am just looking for the overall best and most popular options", prompt)

if __name__ == '__main__':
    unittest.main()
