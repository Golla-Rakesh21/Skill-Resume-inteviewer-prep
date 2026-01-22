import streamlit as st
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
import random

# --- 1. Synthetic Data Generation ---
# In a real-world scenario, you'd have thousands of resume-JD pairs with scores.
# Here, we create a realistic synthetic dataset for our model to learn from.
def create_synthetic_data(all_skills: list, num_samples: int = 500):
    data = []
    for _ in range(num_samples):
        # Create a synthetic job description with 5-10 required skills
        jd_skills = set(random.sample(all_skills, k=random.randint(5, 10)))
        jd_text = " ".join(jd_skills) + " agile environment proactive team player"

        # Create a synthetic resume that matches some of the JD skills
        num_resume_skills = random.randint(2, len(jd_skills))
        resume_skills = set(random.sample(list(jd_skills), k=num_resume_skills))
        
        # Add some non-matching skills
        num_other_skills = random.randint(2, 5)
        other_skills = set(random.sample(all_skills, k=num_other_skills)) - jd_skills
        resume_skills.update(other_skills)
        resume_text = " ".join(resume_skills)

        # Calculate a "true" score based on skill match percentage
        match_ratio = len(jd_skills.intersection(resume_skills)) / len(jd_skills)
        score = int(match_ratio * 100)
        
        # Add some noise to make it more realistic
        score += random.randint(-5, 5)
        score = max(0, min(100, score))

        data.append({"resume_jd_text": resume_text + " " + jd_text, "score": score})
    return pd.DataFrame(data)

# --- 2. Model Training ---
# We use @st.cache_resource to train the model only once and cache it.
@st.cache_resource
def train_ats_model(all_skills: list):
    """
    Generates synthetic data, trains a TF-IDF vectorizer, and a Ridge regression model.
    """
    df = create_synthetic_data(all_skills)
    
    # Feature Engineering: TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
    X = vectorizer.fit_transform(df['resume_jd_text'])
    y = df['score']

    # Model Training
    model = Ridge(alpha=1.0)
    model.fit(X, y)
    
    return vectorizer, model

# --- 3. Contribution Analysis ---
@st.cache_data(show_spinner="Analyzing skill impact...")
def analyze_skill_contributions(resume_text: str, job_desc_text: str, resume_skills: list, _vectorizer, _model):
    """
    Calculates the contribution of each skill to the predicted ATS score.
    """
    if not resume_skills:
        return {}

    combined_text = resume_text + " " + job_desc_text
    
    # Transform the user's text using the trained vectorizer
    text_vector = _vectorizer.transform([combined_text])
    
    # Get the model's learned coefficients (weights)
    coeffs = _model.coef_
    feature_names = _vectorizer.get_feature_names_out()
    
    # Create a mapping from feature name to its weight
    feature_weights = dict(zip(feature_names, coeffs))
    
    # Get the TF-IDF score for each word in the user's text
    text_tfidf_scores = text_vector.toarray().flatten()
    text_feature_scores = dict(zip(feature_names, text_tfidf_scores))
    
    contributions = {}
    for skill in resume_skills:
        skill_lower = skill.lower()
        # Find all features/words related to the skill (e.g., 'node.js' -> 'node', 'js')
        skill_parts = [part for part in skill_lower.split('.') if part] # For 'node.js'
        if not skill_parts:
             skill_parts = [skill_lower]

        total_skill_contribution = 0
        for part in skill_parts:
            if part in feature_weights and part in text_feature_scores:
                # Contribution = (Learned Importance of Word) * (How much of that word is in the text)
                contribution = feature_weights[part] * text_feature_scores[part]
                total_skill_contribution += contribution
        
        contributions[skill] = round(total_skill_contribution, 2)
        
    # Sort by contribution value, descending
    sorted_contributions = dict(sorted(contributions.items(), key=lambda item: item[1], reverse=True))

    return sorted_contributions