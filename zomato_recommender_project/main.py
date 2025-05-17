import streamlit as st
import pandas as pd
import os

from data_preprocessing import load_and_clean_data
from recommender import filter_and_rank
from utils import explain_recommendation, get_map_link

# Set page configuration
st.set_page_config(page_title="Zomato Restaurant Recommender", page_icon="🍽", layout="wide")
st.title("🍽 Knowledge-Based Restaurant Recommender System")

# Cache data loading function
@st.cache_data
def cached_load_and_clean_data(path):
    return load_and_clean_data(path)

# Load data
data_path = "zomato_recommender_project/data/zomato.csv"
df = cached_load_and_clean_data(data_path)

# Validate data
if df is None or df.empty:
    st.error("❌ Failed to load data. Please ensure 'data/zomato.csv' exists and is formatted correctly.")
    st.stop()

# Sidebar - User Preferences
st.sidebar.header("🎯 Set Your Preferences")

# User Input Options
cuisines = [""] + sorted(df['Primary Cuisine'].dropna().unique())
locations = [""] + sorted(df['City'].dropna().unique())

cuisine = st.sidebar.selectbox("🍜 Choose Cuisine", cuisines)
location = st.sidebar.selectbox("📍 Choose City", locations)
price = st.sidebar.selectbox("💰 Select Price Range", ["", "Low", "Medium", "High"])
has_delivery = st.sidebar.checkbox("🚚 Require Online Delivery")

# Recommendation Trigger
if st.sidebar.button("🔍 Recommend"):
    results = filter_and_rank(df, cuisine, location, price, has_delivery)
    st.session_state['results'] = results

# Display Recommendations if Available
if 'results' in st.session_state:
    results = st.session_state['results']

    if results.empty:
        st.warning("⚠ No restaurants match your preferences. Try different filters.")
    else:
        st.subheader("✅ Top Restaurant Matches")

        # Sorting Options
        sort_by = st.selectbox(
            "🔽 Sort By",
            ["Score (Default)", "Rating", "Cost"],
            key="sort_option"
        )

        sort_column = {
            "Score (Default)": "Score",
            "Rating": "Aggregate rating",
            "Cost": "Average Cost for two"
        }[sort_by]

        sorted_results = results.sort_values(
            by=sort_column,
            ascending=True if sort_by == "Cost" else False
        )

        # Display Results
        for idx, row in sorted_results.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.subheader(row['Restaurant Name'])
                    st.markdown(f"*Cuisine:* {row['Primary Cuisine'].title()}  \n"
                                f"*Rating:* {row['Aggregate rating']} ⭐  \n"
                                f"*Cost for Two:* ₹{row['Average Cost for two']}  \n"
                                f"*Votes:* {int(row['Votes'])}  \n"
                                f"*Location:* {row['City']} - {row['Locality']}")
                    st.markdown(f"[📍 View on Google Maps]({get_map_link(row['City'], row['Locality'])})")
                    st.markdown(f"💡 Why Recommended:** {explain_recommendation(row)}")
                with col2:
                    st.write("")  # Placeholder spacing
                    st.button("View Details", key=f"details_{idx}")

            st.markdown("---")

        # CSV Download
        st.download_button(
            label="⬇ Download as CSV",
            data=sorted_results.to_csv(index=False),
            file_name="restaurant_recommendations.csv",
            mime="text/csv"
        )

        st.success("🎉 Recommendations Ready!")
        st.balloons()
