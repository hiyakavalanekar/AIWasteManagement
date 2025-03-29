# rag_utils.py

import pandas as pd
import numpy as np
import faiss
import os
from sentence_transformers import SentenceTransformer


# Load model globally to avoid reloading for every query
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


def build_faiss_index(csv_path="data/combined_lmop_database.csv", index_path="faiss_lmop.index"):
    """
    Builds a FAISS index from landfill metadata and saves both index and chunk metadata.
    """
    lmop_df = pd.read_csv(csv_path)
    lmop_df.dropna(subset=['State', 'City', 'County'], inplace=True)

    # Generate readable chunks from rows
    lmop_df['chunk'] = lmop_df.apply(
        lambda row: f"Landfill in {row['City']}, {row['County']}, {row['State']} (Zip: {row['Zip Code']}):\n"
                    f"Capacity: {row.get('Rated MW Capacity', 'N/A')} MW,\n"
                    f"Methane Flow: {row.get('LFG Flow to Project (mmscfd)', 'N/A')} mmscfd", axis=1)

    chunks = lmop_df['chunk'].tolist()
    embeddings = embedding_model.encode(chunks, show_progress_bar=True)

    # Create FAISS index
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    # Save index and metadata
    faiss.write_index(index, index_path)
    lmop_df.to_csv("data/chunks_with_metadata.csv", index=False)
    print("✅ FAISS index built and saved.")


def retrieve_relevant_chunks(query, top_k=5, index_path="faiss_lmop.index"):
    """
    Retrieves the top-k most relevant text chunks for a given query.
    """
    if not os.path.exists(index_path):
        raise FileNotFoundError("❌ FAISS index not found. Run `build_faiss_index()` first.")

    index = faiss.read_index(index_path)
    df = pd.read_csv("data/chunks_with_metadata.csv")

    # Get query embedding
    query_embedding = embedding_model.encode([query])
    D, I = index.search(np.array(query_embedding), top_k)

    # Retrieve and join relevant chunks
    results = [df.iloc[i]['chunk'] for i in I[0]]
    return "\n\n".join(results)
