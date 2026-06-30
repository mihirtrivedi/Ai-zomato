import pandas as pd
from typing import List, Dict, Any, Optional

def apply_filters(
    df: pd.DataFrame,
    city: Optional[str] = None,
    budget: Optional[str] = None,
    cuisine: Optional[str] = None,
    min_rating: Optional[float] = None,
    rest_type: Optional[str] = None,
    top_n: int = 15
) -> List[Dict[str, Any]]:
    """
    Applies a forgiving scoring system to the dataframe and returns the top N restaurants.
    Returns a list of dictionaries to be easily serialized into JSON for the LLM prompt.
    """
    if df.empty:
        return []

    filtered_df = df.copy()

    # 1. We removed the strict city cutoff to guarantee results for every combination!

    # 2. Forgiving Scoring System
    def calculate_score(row):
        score = 0
        
        # City/Location points (Massive bonus for matching city to prioritize local options)
        if city and pd.notnull(row.get('location')):
            # We use fuzzy matching to account for typos like 'Banglore' vs 'Bangalore'
            loc_str = str(row['location']).lower()
            city_str = city.lower().strip()
            # If the exact city is in the location, or the typo is close enough (simple contains check)
            if city_str in loc_str:
                score += 100
            elif city_str[:4] in loc_str: # Partial match for typos like 'Bang' matching 'Bangalore'
                score += 50
                
        # Base rating points (e.g. 4.5 gives 45 points)
        if pd.notnull(row.get('rating')):
            score += float(row['rating']) * 10
            
            # Penalty for missing min rating (but doesn't instantly delete them)
            if min_rating and float(row['rating']) < min_rating:
                score -= 30
        
        # Cuisine points
        if cuisine and pd.notnull(row.get('cuisine')):
            if cuisine.lower().strip() in str(row['cuisine']).lower():
                score += 30
                
        # Establishment Type points
        if rest_type and rest_type.lower() != "any" and pd.notnull(row.get('rest_type')):
            if rest_type.lower().strip() in str(row['rest_type']).lower():
                score += 25
                
        # Budget points
        if budget and budget.lower() != "any" and pd.notnull(row.get('cost')):
            cost = float(row['cost'])
            b_target = budget.lower().strip()
            if b_target == 'low' and cost <= 500:
                score += 20
            elif b_target == 'medium' and 500 < cost <= 1500:
                score += 20
            elif b_target == 'high' and cost > 1500:
                score += 20
                
        return score

    # Calculate match score for all remaining restaurants in the city
    filtered_df['match_score'] = filtered_df.apply(calculate_score, axis=1)
    
    # Sort by the highest score descending
    filtered_df = filtered_df.sort_values(by='match_score', ascending=False)
    
    # Take top N closest matches
    top_restaurants = filtered_df.head(top_n)
    
    # Replace NaN with None for valid JSON serialization
    top_restaurants = top_restaurants.where(pd.notnull(top_restaurants), None)
    
    return top_restaurants.to_dict(orient='records')
