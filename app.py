import streamlit as st
from data_ingestor import get_cleaned_data
from filter_engine import apply_filters
from prompt_builder import build_system_prompt, build_user_prompt
from llm_client import get_ai_recommendations

# Set page config
st.set_page_config(page_title="AI Zomato Recommender", page_icon="🍔", layout="centered")

@st.cache_data
def load_data():
    return get_cleaned_data()

# Load the dataset once into Streamlit cache
df = load_data()

st.title("🍔 Zomato AI Recommender")
st.markdown("Find the perfect spot for your next meal using AI! 🍕🍣🍷")
st.markdown("---")

# Zomato Filters (Main View)
st.subheader("🎯 Zomato Filters")
col1, col2, col3 = st.columns(3)

with col1:
    city = st.text_input("City (Required)", placeholder="e.g., Mumbai, Bangalore")
    min_rating = st.slider("Minimum Rating", min_value=1.0, max_value=5.0, value=3.5, step=0.1)

with col2:
    rest_type = st.selectbox("Establishment Type", options=["Any", "Restaurant", "Cafe", "Hotel", "Casual Dining", "Quick Bites", "Pub", "Dessert Parlor", "Fine Dining"])
    cuisine = st.text_input("Cuisine Preference", placeholder="e.g., Chinese, Italian")

with col3:
    budget = st.selectbox("Budget Level", options=["Any", "Low", "Medium", "High"])

st.markdown("---")

# Main container for the unstructured "Nuance"
st.subheader("What exactly are you looking for? 🕵️‍♂️")
nuance = st.text_area(
    "Describe your ideal dining experience, occasion, or specific vibe:",
    placeholder="e.g., I need a quiet, dimly lit place for a romantic anniversary dinner with live music."
)

if st.button("Generate AI Recommendations ✨", type="primary", use_container_width=True):
    if not city:
        st.error("Please enter a City to begin!")
    elif df is None or df.empty:
        st.error("🚨 Dataset not loaded properly.")
    else:
        with st.spinner("Our AI food critic is evaluating the best options..."):
            
            b_val = None if budget == "Any" else budget.lower()
            c_val = None if not cuisine else cuisine
            r_val = None if rest_type == "Any" else rest_type.lower()
            
            # 1. Deterministic Filtering
            filtered_restaurants = apply_filters(
                df=df,
                city=city,
                budget=b_val,
                cuisine=c_val,
                min_rating=min_rating,
                rest_type=r_val,
                top_n=15
            )
            
            # Edge case: No results from hard filter
            if not filtered_restaurants:
                st.info("🤷‍♂️ No restaurants found matching your strict criteria (City, Budget, Cuisine). Try broadening your search.")
            else:
                # 2. Prompt Building
                system_prompt = build_system_prompt()
                user_prompt = build_user_prompt(nuance=nuance, restaurants=filtered_restaurants)
                
                # 3. LLM Call natively within Streamlit
                ai_recommendations = get_ai_recommendations(system_prompt=system_prompt, user_prompt=user_prompt)
                
                # Edge case: LLM fails or times out
                if not ai_recommendations:
                    st.warning("⚠️ AI service is currently unavailable. Displaying top filtered results instead.")
                    st.success("🎉 Here are your top recommendations!")
                    
                    for idx, rec in enumerate(filtered_restaurants[:3], 1):
                        with st.expander(f"#{idx} - {rec.get('name', 'Unknown')}", expanded=True):
                            st.markdown("**AI Reasoning:**")
                            st.write("*This is a top-rated choice based on your strict filters. (AI explanation currently unavailable).*")
                else:
                    st.success("🎉 Here are your top recommendations!")
                    
                    for idx, rec in enumerate(ai_recommendations, 1):
                        with st.expander(f"#{idx} - {rec.get('name', 'Unknown')}", expanded=True):
                            st.markdown("**AI Reasoning:**")
                            st.write(f"*{rec.get('reason', 'No explanation provided.')}*")
