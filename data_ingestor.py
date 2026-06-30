import os
import pandas as pd
from datasets import load_dataset

DATA_FILE = "zomato_cleaned.csv"

def get_cleaned_data() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        print("Loading cached dataset from disk...")
        df = pd.read_csv(DATA_FILE)
        return df
        
    print("Streaming dataset from Hugging Face (fetching 5000 rows for speed)...")
    try:
        dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train", streaming=True)
        records = []
        for i, row in enumerate(dataset):
            records.append(row)
            if i >= 5000:
                break
        df = pd.DataFrame(records)
    except Exception as e:
        print(f"Failed to download dataset: {e}")
        return pd.DataFrame()
    
    # Normalize column names to lowercase and strip whitespace
    df.columns = [col.lower().strip() for col in df.columns]
    
    # Mapping potential column variations
    col_mapping = {}
    if 'approx_cost(for two people)' in df.columns:
        col_mapping['approx_cost(for two people)'] = 'cost'
    if 'rate' in df.columns:
        col_mapping['rate'] = 'rating'
    if 'cuisines' in df.columns:
        col_mapping['cuisines'] = 'cuisine'
        
    df.rename(columns=col_mapping, inplace=True)
    
    # Drop rows where critical information is missing
    critical_cols = [col for col in ['name', 'location', 'rating', 'cost', 'cuisine'] if col in df.columns]
    df.dropna(subset=critical_cols, inplace=True)
    
    # Normalize text columns
    for col in ['name', 'location', 'cuisine', 'rest_type', 'listed_in(type)']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()
            
    # Combine or map rest_type if needed. The raw data often has 'rest_type' or 'listed_in(type)'
    if 'rest_type' not in df.columns and 'listed_in(type)' in df.columns:
        df['rest_type'] = df['listed_in(type)']
            
    # Format Cost (e.g. '1,200' -> 1200.0)
    if 'cost' in df.columns:
        df['cost'] = df['cost'].astype(str).str.replace(',', '', regex=False).str.extract(r'(\d+)')[0].astype(float)
        
    # Format Rating (e.g. '4.1/5' -> 4.1)
    if 'rating' in df.columns:
        df['rating'] = df['rating'].astype(str).str.extract(r'(\d+\.\d+|\d+)')[0].astype(float)
        
    # Drop rows that failed conversion
    if 'cost' in df.columns:
        df.dropna(subset=['cost'], inplace=True)
    if 'rating' in df.columns:
        df.dropna(subset=['rating'], inplace=True)
        
    print(f"Dataset cleaned. {len(df)} rows remaining.")
    
    # Save to disk to cache
    df.to_csv(DATA_FILE, index=False)
    print(f"Dataset cached to {DATA_FILE}")
    
    return df

if __name__ == "__main__":
    df = get_cleaned_data()
    print(df.head())
    print("Unique Types:", df.get('rest_type', pd.Series()).unique()[:20])
