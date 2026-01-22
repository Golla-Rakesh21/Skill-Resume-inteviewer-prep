import json
from pathlib import Path
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Use a singleton pattern for the model to avoid reloading it
@st.cache_resource
def get_sentence_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_data(show_spinner="Loading and analyzing skill data...")
def analyze_skill_clusters(skill: str):
    """
    Loads resume snippets for a skill, embeds them, clusters them, and analyzes the clusters.
    """
    # 1. Load Data
    data_path = Path("data/resume_snippets.json")
    if not data_path.exists():
        return None, "Error: `data/resume_snippets.json` not found."
    
    with open(data_path, "r") as f:
        all_snippets = json.load(f)
    
    snippets = all_snippets.get(skill)
    if not snippets or len(snippets) < 3: # Need at least 3 snippets to form 3 clusters
        return None, f"Not enough data for the skill '{skill}'. Add more snippets to `data/resume_snippets.json`."

    # 2. Vectorize (Embed)
    model = get_sentence_model()
    embeddings = model.encode(snippets)

    # 3. Cluster
    # We assume 3 clusters: Beginner, Intermediate, Advanced
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    kmeans.fit(embeddings)
    cluster_labels = kmeans.labels_

    # 4. Analyze and Interpret Clusters
    clusters = {i: [] for i in range(3)}
    for i, snippet in enumerate(snippets):
        clusters[cluster_labels[i]].append(snippet)
    
    # Analyze keywords and determine proficiency level for each cluster
    cluster_insights = {}
    term_strengths = []
    for i in range(3):
        # Use TF-IDF to find top keywords
        tfidf = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = tfidf.fit_transform(clusters[i])
            feature_names = np.array(tfidf.get_feature_names_out())
            # Get the score for each term in each document, then average
            avg_scores = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
            # Sort and get top 5
            top_indices = avg_scores.argsort()[-5:][::-1]
            top_keywords = feature_names[top_indices].tolist()
            
            # Heuristic to label clusters: The cluster with more "advanced" words gets a higher score
            advanced_words = ["architect", "led", "optimized", "scalable", "distributed", "pipeline", "migration", "mentored"]
            strength = sum(snippet.count(word) for snippet in clusters[i] for word in advanced_words)
            term_strengths.append((i, strength))

        except ValueError: # Happens if a cluster has only stop words
            top_keywords = ["-"]
            term_strengths.append((i, 0))

        cluster_insights[i] = {
            "keywords": top_keywords,
            "snippets": clusters[i][:3] # Show up to 3 example snippets
        }
    
    # Sort clusters by strength to assign proficiency labels
    sorted_clusters = sorted(term_strengths, key=lambda item: item[1])
    proficiency_map = {
        sorted_clusters[0][0]: "Beginner",
        sorted_clusters[1][0]: "Intermediate",
        sorted_clusters[2][0]: "Advanced"
    }

    # Prepare final result
    final_result = {
        proficiency_map[i]: data for i, data in cluster_insights.items()
    }

    return final_result, None

def predict_user_snippet_level(user_snippet: str, skill: str):
    """
    Predicts the proficiency level of a user's snippet by finding the closest cluster.
    This function would be more robust if it reused the trained KMeans object,
    but for this stateless app, we recalculate for simplicity.
    """
    # This is a simplified version. A production system would save and reuse the kmeans model.
    _, error = analyze_skill_clusters(skill) # Ensure data exists and is processed
    if error:
        return error

    data_path = Path("data/resume_snippets.json")
    with open(data_path, "r") as f:
        snippets = json.load(f).get(skill, [])
    
    model = get_sentence_model()
    embeddings = model.encode(snippets)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto').fit(embeddings)
    
    user_embedding = model.encode([user_snippet])
    prediction = kmeans.predict(user_embedding)[0]

    # Re-run the analysis part to get the same proficiency map
    term_strengths = []
    for i in range(3):
        cluster_snippets = [s for j, s in enumerate(snippets) if kmeans.labels_[j] == i]
        advanced_words = ["architect", "led", "optimized", "scalable", "distributed", "pipeline", "migration", "mentored"]
        strength = sum(s.count(word) for s in cluster_snippets for word in advanced_words)
        term_strengths.append((i, strength))
    
    sorted_clusters = sorted(term_strengths, key=lambda item: item[1])
    proficiency_map = {
        sorted_clusters[0][0]: "Beginner",
        sorted_clusters[1][0]: "Intermediate",
        sorted_clusters[2][0]: "Advanced"
    }

    return f"Your description aligns most closely with the **{proficiency_map[prediction]}** cluster."