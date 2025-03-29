import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("combined_lmop_database.csv")

# Function to get policy recommendations
def get_policies(state, city=None):
    subset = df[df['State'] == state]
    if city:
        subset = subset[subset['City'] == city]
    
    open_landfills = subset[subset['Current Landfill Status'] == 'Open'].shape[0]
    closed_landfills = subset[subset['Current Landfill Status'] == 'Closed'].shape[0]
    energy_projects = subset['LFG Energy Project Type'].notna().sum()
    
    policies = []
    if closed_landfills > open_landfills:
        policies.append("Repurpose closed landfills for renewable energy projects.")
    if energy_projects < open_landfills:
        policies.append("Increase landfill gas-to-energy initiatives for active landfills.")
    if open_landfills > 50:
        policies.append("Implement stricter waste reduction and recycling programs.")
    if not policies:
        policies.append("Maintain current landfill management strategies.")
    
    return policies, open_landfills, closed_landfills, energy_projects

# Streamlit UI
st.title("Landfill Policy Recommendation Dashboard")

state = st.text_input("Enter State Name:")
city = st.text_input("(Optional) Enter City Name:")

if state:
    policies, open_count, closed_count, energy_count = get_policies(state, city)
    
    st.subheader(f"Landfill Overview for {city+', ' if city else ''}{state}")
    st.write(f"**Open Landfills:** {open_count}")
    st.write(f"**Closed Landfills:** {closed_count}")
    st.write(f"**Landfills with Energy Projects:** {energy_count}")
    
    st.subheader("Suggested Policies:")
    for policy in policies:
        st.markdown(f"- {policy}")
    
    # Visualization
    fig = px.bar(x=['Open', 'Closed', 'With Energy Projects'],
                 y=[open_count, closed_count, energy_count],
                 labels={'x': "Landfill Status", 'y': "Count"},
                 title="Landfill Distribution",
                 color=['Open', 'Closed', 'With Energy Projects'])
    st.plotly_chart(fig)
