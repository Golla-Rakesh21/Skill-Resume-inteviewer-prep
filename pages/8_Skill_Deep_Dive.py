import streamlit as st
from utils.insights import analyze_skill_clusters, predict_user_snippet_level
import json
from pathlib import Path

st.set_page_config(page_title="Skill Deep Dive", page_icon="🔬", layout="wide")
st.title("🔬 Skill Deep Dive & Career Path")
st.info(
    "Explore what different proficiency levels look like for a skill, based on real-world data. "
    "This tool uses unsupervised machine learning to cluster and analyze project descriptions."
)

# Load available skills from the snippets data
try:
    with open(Path("data/resume_snippets.json"), "r") as f:
        available_skills = list(json.load(f).keys())
except FileNotFoundError:
    st.error("`data/resume_snippets.json` not found. This feature cannot run.")
    st.stop()

selected_skill = st.selectbox("Select a skill to analyze:", available_skills)

if selected_skill:
    insights, error = analyze_skill_clusters(selected_skill)
    
    if error:
        st.error(error)
    elif insights:
        st.header(f"Analysis for: {selected_skill}")

        # Define order for display
        levels = ["Beginner", "Intermediate", "Advanced"]
        
        for level in levels:
            if level in insights:
                with st.expander(f"**{level} Level** - Representative Keywords: `{', '.join(insights[level]['keywords'])}`"):
                    st.markdown("**Common Project Descriptions:**")
                    for snippet in insights[level]['snippets']:
                        st.markdown(f"- *{snippet}*")
        
        st.header("Analyze Your Own Experience")
        user_snippet = st.text_area(
            "Paste one of your resume bullet points for this skill:",
            height=100,
            placeholder=f"e.g., Developed a new feature for the main application using {selected_skill}..."
        )

        if st.button("Analyze My Bullet Point"):
            if user_snippet and user_snippet.strip():
                with st.spinner("Classifying your experience..."):
                    result = predict_user_snippet_level(user_snippet, selected_skill)
                    st.success(result)
            else:
                st.warning("Please enter a bullet point to analyze.")