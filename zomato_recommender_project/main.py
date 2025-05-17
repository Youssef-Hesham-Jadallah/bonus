import streamlit as st
import pandas as pd
import os

from data_preprocessing import load_and_clean_data
from recommender import filter_and_rank
from utils import explain_recommendation, get_map_link

# Set page configuration
st.set_page_config(page_title="Zomato Restaurant Recommender", page_icon="🍽️", layout="wide")
st.title("🍽️ Knowledge-Based Restaurant Recommender System")

# Cache data loading function
@st.cache_data
def cached_load_and_clean_data(path):
    return load_and_clean_data(path)

# Load data
data_path = "zomato_recommender_project/data/zomato.csv"
df = cached_load_and_clean_data(data_path)

# Check if data is loaded
if df is None or df.empty:
    st.error("❌ Failed to load data. Please ensure that 'data/zomato.csv' exists and is properly formatted.")
    st.stop()

# Sidebar - User Preferences
st.sidebar.header("🎯 Set Your Preferences")

cuisines = [""] + sorted(df['Primary Cuisine'].dropna().unique())
locations = [""] + sorted(df['City'].dropna().unique())
cuisine = st.sidebar.selectbox("🍜 Cuisine", cuisines)
location = st.sidebar.selectbox("📍 City", locations)
price = st.sidebar.selectbox("💰 Price Range", ["", "Low", "Medium", "High"])
has_delivery = st.sidebar.checkbox("🚚 Online Delivery Available")

# Recommend button
if st.sidebar.button("🔍 Recommend"):
    results = filter_and_rank(df, cuisine, location, price, has_delivery)
    st.session_state['results'] = results

    if results.empty:
        st.warning("⚠️ No matching restaurants found. Try adjusting your preferences.")
    else:
        st.subheader("✅ Top Matching Restaurants")

        # Sorting options
        sort_option = st.selectbox(
            "🔽 Sort Results By",
            ["Score (Default)", "Rating", "Cost"],
            key="sort_option"
        )

        sort_by_column = {
            "Score (Default)": "Score",
            "Rating": "Aggregate rating",
            "Cost": "Average Cost for two"
        }[sort_option]

        sorted_results = results.sort_values(by=sort_by_column, ascending=False if sort_option != "Cost" else True)

        # Display results
        for idx, row in sorted_results.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.subheader(row['Restaurant Name'])
                    st.markdown(f"**Cuisine:** {row['Primary Cuisine'].title()} | **Rating:** {row['Aggregate rating']} ⭐")
                    st.markdown(f"**Cost for Two:** ₹{row['Average Cost for two']} | **Votes:** {int(row['Votes'])}")
                    st.markdown(f"**Location:** {row['City']} - {row['Locality']}")
                    map_link = get_map_link(row['City'], row['Locality'])
                    st.markdown(f"[📍 Open in Google Maps]({map_link})")
                    st.markdown(f"**💡 Explanation:** _{explain_recommendation(row)}_")
                with col2:
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    st.button("View Details", key=f"details_{idx}")
            st.markdown("---")

        # Download button
        csv = sorted_results.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Recommendations",
            data=csv,
            file_name="recommendations.csv",
            mime="text/csv"
        )

        st.success("🎉 Recommendations generated successfully!")
        st.balloons()
