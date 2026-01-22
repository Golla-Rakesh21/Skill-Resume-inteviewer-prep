import streamlit as st
from utils.optimizer import optimize_bullet_point

st.set_page_config(page_title="Resume Optimizer", page_icon="✨", layout="wide")
st.title("✨ AI Resume Optimizer")

st.info("Paste a single bullet point from your resume to get AI-powered suggestions for improvement.")

# Get context from the job description if it exists
job_desc = st.session_state.get("job_desc", "")
if not job_desc:
    st.warning("For the best results, paste a job description on the main page first. The AI will use it for context.")

# User input
st.header("Your Resume Bullet Point")
original_bullet = st.text_area(
    "Enter the bullet point you want to improve:",
    placeholder="e.g., Worked on the front-end part of the main project using React.",
    height=100
)

if st.button("🚀 Optimize This Bullet Point", type="primary"):
    if original_bullet and original_bullet.strip():
        suggestions = optimize_bullet_point(original_bullet, job_desc)
        st.header("✅ Here are your optimized suggestions:")
        st.markdown(suggestions)
    else:
        st.error("Please enter a bullet point to optimize.")