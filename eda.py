# eda.py
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def run_eda(df):
    st.markdown("### 🧠 Key Metrics")
    st.write(f"**Total Landfills:** {df['Landfill ID'].nunique()}")
    st.write(f"**States Covered:** {df['State'].nunique()}")
    st.write(f"**Unique Counties:** {df['County'].nunique()}")

    st.markdown("### 🗺️ Top 10 States by Landfill Count")
    state_counts = df['State'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=state_counts.values, y=state_counts.index, palette="viridis", ax=ax)
    ax.set_xlabel("Number of Landfills")
    ax.set_ylabel("State")
    ax.set_title("Top 10 States by Landfill Count")
    st.pyplot(fig)

    st.markdown("### ⚡ Methane Emissions Distribution")
    if "LFG Flow to Project (mmscfd)" in df.columns:
        fig, ax = plt.subplots()
        sns.histplot(df["LFG Flow to Project (mmscfd)"].dropna(), bins=30, kde=True, color="darkorange", ax=ax)
        ax.set_title("Distribution of Methane Flow (mmscfd)")
        ax.set_xlabel("Methane Flow (mmscfd)")
        st.pyplot(fig)
    else:
        st.warning("Methane flow data not available.")

    st.markdown("### 🏗️ Rated MW Capacity by State (Top 10)")
    if "Rated MW Capacity" in df.columns:
        top_states = df.groupby("State")["Rated MW Capacity"].mean().nlargest(10).reset_index()
        fig, ax = plt.subplots()
        sns.barplot(data=top_states, x="Rated MW Capacity", y="State", palette="magma", ax=ax)
        ax.set_title("Avg Rated MW Capacity by Top 10 States")
        ax.set_xlabel("Rated MW Capacity")
        st.pyplot(fig)
    else:
        st.warning("Rated MW Capacity data not available.")

    st.markdown("### 📊 Boxplot: Rated MW Capacity (Outlier Detection)")
    if "Rated MW Capacity" in df.columns:
        fig, ax = plt.subplots()
        sns.boxplot(x=df["Rated MW Capacity"].dropna(), color="teal", ax=ax)
        ax.set_title("Rated MW Capacity Boxplot")
        st.pyplot(fig)

    st.markdown("### 🔄 Correlation: Methane Flow vs MW Capacity")
    if "LFG Flow to Project (mmscfd)" in df.columns and "Rated MW Capacity" in df.columns:
        fig, ax = plt.subplots()
        sns.scatterplot(
            data=df, 
            x="LFG Flow to Project (mmscfd)", 
            y="Rated MW Capacity",
            hue="State", 
            alpha=0.7, 
            ax=ax,
            legend=False
        )
        ax.set_title("Methane Flow vs MW Capacity")
        st.pyplot(fig)
