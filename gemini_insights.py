# gemini_insights.py
from gemini_client import get_gemini_chat
from rag_utils import retrieve_relevant_chunks

# Persistent chat session from gemini_client
chat = get_gemini_chat()

# Generate insights using enhanced prompt and RAG-based context
def get_policy_insights(state, county, city, zipcode, filtered_df):
    methane = filtered_df['LFG Flow to Project (mmscfd)'].mean()
    capacity = filtered_df['Rated MW Capacity'].mean()
    landfills = filtered_df['Landfill ID'].nunique()

    # RAG-enhanced context
    try:
        faiss_context = retrieve_relevant_chunks(
            query=f"{city} {county} {state} landfill methane policy",
            top_k=5
        )
    except Exception as e:
        faiss_context = "⚠️ Could not retrieve external context. Proceeding with available data only."

    # Methane-based policy alert
    alert = ""
    if methane > 5:
        alert = "⚠️ Methane flow is critically high. Recommend carbon offset programs and enhanced capture infrastructure."
    elif methane < 1:
        alert = "ℹ️ Methane flow is minimal. Focus on waste minimization and circular practices."

    # Final engineered prompt
    prompt = f"""
📍 REGION CONTEXT:
- State: {state}
- County: {county}
- City: {city}
- Zip Code: {zipcode}

📊 DATA SNAPSHOT:
- Total Landfills: {landfills}
- Avg Methane Flow: {methane:.2f} mmscfd
- Avg MW Capacity: {capacity:.2f} MW

{alert}

🔎 CONTEXTUAL SNAPSHOTS (from similar landfills via FAISS):
{faiss_context}

🧠 STRATEGIC DIRECTIVES:
1. Suggest AI-integrated landfill management strategies.
2. Recommend policy alignments with ESG and SDG targets.
3. Estimate energy potential using methane-to-electricity conversion.
4. Propose public-private partnership models for renewable infrastructure.
5. Include predictive modeling suggestions for methane forecasting.

🎯 Your insights should be layered, region-specific, and leverage the latest waste-tech frameworks.
    """

    # Optional prompt logging
    try:
        with open("prompt_logs.txt", "a", encoding="utf-8") as f:
            f.write(f"--- PROMPT for {city}, {state} ---\n{prompt}\n\n")
    except Exception as log_error:
        print("🛑 Failed to write prompt to log:", log_error)

    # Send to Gemini
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini API error: {str(e)}"
