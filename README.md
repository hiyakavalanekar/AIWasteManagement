# AIWasteManagement

# ♻️ AI-Powered Landfill Management Dashboard

## Overview
This project is an interactive dashboard that uses AI to analyze landfill data from across the United States. It helps policymakers and researchers understand landfill patterns, methane emissions, and energy potential, and provides region-specific recommendations using Google’s Gemini API and RAG (Retrieval-Augmented Generation) with FAISS.

---

## Features
- Filter landfill data by State, County, City, and Zip Code
- View interactive visualizations of:
  - Methane emissions
  - MW capacity
  - Landfill distribution
- Get AI-powered policy suggestions using Gemini
- Retrieve relevant context using FAISS for better insights
- Clean UI built with Streamlit

---

## Folder Structure

├── app.py # Main Streamlit app ├── eda.py # Visualizations and analysis ├── gemini_insights.py # AI prompt + response logic ├── gemini_client.py # Gemini model setup ├── rag_utils.py # FAISS indexing and search ├── data/ │ └── combined_lmop_database.csv │ └── chunks_with_metadata.csv ├── faiss_lmop.index # Vector index file ├── .env # Gemini API key ├── prompt_logs.txt # Optional log file └── requirements.txt # Python dependencies


---

## How to Run

1. **Clone the repo**
git clone https://github.com/your-username/ai-landfill-dashboard.git cd ai-landfill-dashboard


2. **Install dependencies**
pip install -r requirements.txt


3. **Set your Gemini API key**  
Create a `.env` file in the root folder and add:
GOOGLE_API_KEY=your_api_key_here


4. **Build FAISS index**
python -c "from rag_utils import build_faiss_index; build_faiss_index()"


5. **Run the app**
streamlit run app.py


---

## Tech Stack
- Python
- Streamlit
- SentenceTransformers
- FAISS
- Google Generative AI (Gemini)
- Matplotlib / Seaborn

---

