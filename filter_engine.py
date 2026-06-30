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
    Applies deterministic filters to the dataframe and returns the top N restaurants.
    Returns a list of dictionaries to be easily serialized into JSON for the LLM prompt.
    """
    if df.empty:
        return []

    filtered_df = df.copy()

    # 1. Filter by City (Location)
    if city and 'location' in filtered_df.columns:
        # Case insensitive partial match
        filtered_df = filtered_df[filtered_df['location'].str.contains(city.lower().strip(), case=False, na=False)]

    # 2. Filter by Cuisine
    if cuisine and 'cuisine' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['cuisine'].str.contains(cuisine.lower().strip(), case=False, na=False)]

    # 3. Filter by Budget
    # Assuming Indian Rupees. Low <= 500, Medium 501-1500, High > 1500
    if budget and 'cost' in filtered_df.columns:
        budget = budget.lower().strip()
        if budget == 'low':
            filtered_df = filtered_df[filtered_df['cost'] <= 500]
        elif budget == 'medium':
            filtered_df = filtered_df[(filtered_df['cost'] > 500) & (filtered_df['cost'] <= 1500)]
        elif budget == 'high':
            filtered_df = filtered_df[filtered_df['cost'] > 1500]

    # 4. Filter by Minimum Rating
    if min_rating is not None and 'rating' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

    # 4.5. Filter by Establishment Type
    if rest_type and 'rest_type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['rest_type'].str.contains(rest_type.lower().strip(), case=False, na=False)]

    # 5. Sort by rating (descending) and cost (ascending) to get the best value options
    if 'rating' in filtered_df.columns and 'cost' in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by=['rating', 'cost'], ascending=[False, True])
    elif 'rating' in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by='rating', ascending=False)

    # 6. Take top N
    top_restaurants = filtered_df.head(top_n)
    
    # Replace NaN with None for valid JSON serialization later
    top_restaurants = top_restaurants.where(pd.notnull(top_restaurants), None)
    
    return top_restaurants.to_dict(orient='records')
