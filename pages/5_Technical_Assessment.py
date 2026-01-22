import streamlit as st
import os
from utils.assessment import generate_assessment

st.set_page_config(page_title="Technical Assessment", page_icon="📝", layout="wide")
st.title("📝 Technical Assessment Generator")
st.info("This feature uses the Google AI API to generate a technical quiz based on your skills.")

# --- State Initialization ---
if "assessment_questions" not in st.session_state:
    st.session_state.assessment_questions = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "assessment_submitted" not in st.session_state:
    st.session_state.assessment_submitted = False

# --- API Key Check ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key not configured. Please add it to your `.env` file.")
    st.markdown("You can get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).")
    st.stop()

# --- Skill Selection ---
skills = st.session_state.get("resume_skills", [])
if not skills:
    st.warning("No skills found. Please upload your resume on the main page first.")
    st.stop()

st.header("1. Configure Your Assessment")

col1, col2, col3 = st.columns(3)
with col1:
    selected_skills = st.multiselect("Select skills for the assessment:", skills, default=skills[:2])
with col2:
    difficulty = st.selectbox("Select difficulty:", ["Beginner", "Intermediate", "Advanced"], index=1)
with col3:
    num_questions = st.slider("Number of questions:", 2, 10, 5)

if st.button("🚀 Generate New Assessment", type="primary"):
    if not selected_skills:
        st.error("Please select at least one skill.")
    else:
        # Reset previous assessment state
        st.session_state.assessment_questions = []
        st.session_state.user_answers = {}
        st.session_state.assessment_submitted = False
        
        # Generate new questions and store them in session state
        st.session_state.assessment_questions = generate_assessment(selected_skills, difficulty, num_questions)
        if not st.session_state.assessment_questions:
            st.error("Failed to generate assessment. Please try again.")

# --- Display Assessment Form ---
if st.session_state.assessment_questions and not st.session_state.assessment_submitted:
    st.header("2. Take the Assessment")
    with st.form("assessment_form"):
        user_answers = {}
        for i, q in enumerate(st.session_state.assessment_questions):
            st.markdown(f"**Question {i+1}:** {q['question']}")
            # The key must be unique for each question
            user_answers[i] = st.radio("Choose your answer:", q['options'], key=f"q_{i}", index=None)
            st.markdown("---")
        
        submitted = st.form_submit_button("Submit Answers")
        if submitted:
            st.session_state.user_answers = user_answers
            st.session_state.assessment_submitted = True
            st.rerun()

# --- Display Results ---
if st.session_state.assessment_submitted:
    st.header("3. Assessment Results")
    
    score = 0
    total_qs = len(st.session_state.assessment_questions)
    
    for i, q in enumerate(st.session_state.assessment_questions):
        user_ans = st.session_state.user_answers.get(i)
        correct_ans = q['correct_answer']
        
        if user_ans == correct_ans:
            score += 1
            with st.container(border=True):
                st.success(f"**Question {i+1}: Correct!**")
                st.markdown(f"> {q['question']}")
                st.write(f"Your answer: **{user_ans}**")
        else:
            with st.container(border=True):
                st.error(f"**Question {i+1}: Incorrect**")
                st.markdown(f"> {q['question']}")
                st.write(f"Your answer: **{user_ans if user_ans else 'Not answered'}**")
                st.write(f"Correct answer: **{correct_ans}**")
                st.info(f"**Explanation:** {q['explanation']}")
    
    st.sidebar.metric("Your Score", f"{score}/{total_qs} ({score/total_qs:.0%})")
    
    if st.button("Take Another Assessment"):
        # Clear state to allow a new assessment to be generated
        st.session_state.assessment_questions = []
        st.session_state.user_answers = {}
        st.session_state.assessment_submitted = False
        st.rerun()