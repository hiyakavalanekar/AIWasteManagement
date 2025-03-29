import streamlit as st
import pandas as pd
from eda import run_eda
from gemini_insights import get_policy_insights
from dotenv import load_dotenv
load_dotenv()

# Load dataset
df = pd.read_csv("data/combined_lmop_database.csv")

st.set_page_config(layout="wide", page_title="AI-Powered Landfill Management Dashboard")
st.title("♻️ AI-Powered Landfill Management Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Select Filters")
state = st.sidebar.selectbox("Select State", sorted(df['State'].dropna().unique()))
filtered_df = df[df["State"] == state]

county = st.sidebar.selectbox("Select County", sorted(filtered_df['County'].dropna().unique()))
filtered_df = filtered_df[filtered_df["County"] == county]

city = st.sidebar.selectbox("Select City", sorted(filtered_df['City'].dropna().unique()))
filtered_df = filtered_df[filtered_df["City"] == city]

zipcode = st.sidebar.selectbox("Select Zip Code", sorted(filtered_df['Zip Code'].dropna().unique()))
filtered_df = filtered_df[filtered_df["Zip Code"] == zipcode]

st.subheader(f"📍 Landfill Data for {city}, {state}")
st.dataframe(filtered_df)

# Insights from Gemini
if st.button("🔮 Get AI-Powered Policy Recommendations"):
    with st.spinner("Talking to Gemini..."):
        insight = get_policy_insights(state, county, city, zipcode, filtered_df)
        st.markdown(insight, unsafe_allow_html=True)

# EDA section
st.markdown("---")
st.subheader("📊 Explore Landfill Data")

use_filtered = st.checkbox("Apply selected filters to EDA", value=False)

if use_filtered:
    run_eda(filtered_df)
else:
    run_eda(df)
