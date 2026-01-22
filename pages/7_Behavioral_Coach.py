import streamlit as st
from utils.behavioral import generate_behavioral_questions

st.set_page_config(page_title="Behavioral Coach", page_icon="💬", layout="wide")
st.title("💬 Behavioral Question Coach")

st.info(
    "Prepare for the non-technical part of your interview. "
    "This tool analyzes the job description to generate likely behavioral questions and guides you on how to answer them effectively."
)

# Check for the job description in session state
job_desc = st.session_state.get("job_desc", "")
if not job_desc or not job_desc.strip():
    st.warning("To generate tailored behavioral questions, please go to the main page and paste a Job Description first.")
    st.stop()

st.header("Interview Preparation Guide")
st.markdown(
    """
Behavioral questions are used by interviewers to assess your past performance as an indicator of your future success. The best way to answer them is by using the **STAR method**:

-   **S**ituation: Set the scene and give the necessary details of your example.
-   **T**ask: Describe what your responsibility was in that situation.
-   **A**ction: Explain exactly what steps you took to address it.
-   **R**esult: Share what outcomes your actions achieved.
"""
)

if st.button("🚀 Generate My Questions & Guidance", type="primary"):
    questions_and_guidance = generate_behavioral_questions(job_desc)

    st.header("Your Personalized Behavioral Questions")
    if "Error:" in questions_and_guidance:
        st.error(questions_and_guidance)
    else:
        st.markdown(questions_and_guidance)

        st.success("**Pro Tip:** Practice answering these questions out loud. Write down your STAR stories for each one so you are prepared!")