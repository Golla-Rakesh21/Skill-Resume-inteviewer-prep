import os
import json
import streamlit as st
from dotenv import load_dotenv
from utils.parser import extract_text
from utils.skills import load_taxonomy, build_skill_index, fuzzy_find_skills, compare_with_job_desc
from utils.proficiency import proficiency_score, level_from_scores
from utils.ats import calculate_ats_score # Import the new function

st.set_page_config(page_title="Resume Interviewer", page_icon="🗂️", layout="wide")
load_dotenv()

# ... (keep all the session_state initialization code as is) ...
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []
if "proficiency" not in st.session_state:
    st.session_state.proficiency = {}
if "job_desc" not in st.session_state:
    st.session_state.job_desc = ""
# Initialize generated_qa for the multipage app structure
if "generated_qa" not in st.session_state:
    st.session_state.generated_qa = {}


st.title("🗂️ Resume → Skills → Adaptive Interview")

with st.sidebar:
    # ... (keep the sidebar code as is) ...
    st.header("Upload")
    f = st.file_uploader("Upload your resume (PDF/DOCX)", type=["pdf","docx"])
    if f is not None:
        content = f.read()
        text = extract_text(content, f.name)
        if text:
            st.session_state.resume_text = text
            st.success("Resume parsed successfully.")
            # Clear questions/answers if a new resume is uploaded
            st.session_state.generated_qa = {}
        else:
            st.error("Unsupported file or failed to parse.")

    st.header("Job Description (optional)")
    st.session_state.job_desc = st.text_area(
        "Paste a job description to do gap analysis",
        st.session_state.job_desc,
        height=150
    )


# load taxonomy
TAXO_PATH = os.path.join("data", "skills_taxonomy.json")
taxonomy = load_taxonomy(TAXO_PATH)
all_skills = build_skill_index(taxonomy)
# Save to session state for other pages
st.session_state.taxonomy = taxonomy
st.session_state.all_skills = all_skills


# ... (keep the tab definitions as is) ...
tab1, tab2 = st.tabs(["1) Analysis & Scoring", "2) Next Steps"])


with tab1:
    # --- NEW: ATS Score Section ---
    if st.session_state.job_desc and st.session_state.resume_text:
        st.subheader("📊 ATS Match Score")
        with st.spinner("Calculating ATS score..."):
            ats_results = calculate_ats_score(
                st.session_state.resume_text,
                st.session_state.job_desc,
                all_skills
            )

            score = ats_results['total_score']

            # Display the score with a color-coded progress bar
            st.progress(score / 100)
            st.metric(label="Your Resume's Match Score", value=f"{score}%")

            with st.expander("See Detailed Breakdown"):
                st.markdown("---")
                # Skill Match
                sm = ats_results['skill_match']
                st.markdown(f"**Skill Match: {sm['score']}%** ({sm['details']})")
                st.markdown("_Tip: Ensure the key skills and technologies from the job description are explicitly listed in your resume._")
                st.markdown("---")

                # Keyword Density
                kd = ats_results['keyword_density']
                st.markdown(f"**Contextual Keywords: {kd['score']}%** ({kd['details']})")
                st.markdown("_Tip: Mirror important non-skill terms from the job description, like 'agile environment' or 'B2B platform'._")
                st.markdown("---")

                # Action Verbs
                av = ats_results['action_verbs']
                st.markdown(f"**Action Verbs: {av['score']}%** ({av['details']})")
                st.markdown("_Tip: Start your bullet points with strong verbs like 'Developed', 'Managed', or 'Optimized' to show impact._")
                st.markdown("---")

                # Measurable Metrics
                mm = ats_results['measurable_metrics']
                st.markdown(f"**Quantifiable Results: {mm['score']}%** ({mm['details']})")
                st.markdown("_Tip: Add numbers to show the scale of your achievements (e.g., 'improved performance by 20%', 'managed a $50k budget')._")


    st.subheader("Extracted Skills")
    if st.session_state.resume_text:
        # ... (keep the rest of the skill extraction and proficiency code as is) ...
        resume_skills = fuzzy_find_skills(
            st.session_state.resume_text,
            all_skills,
            threshold=85
        )
        st.session_state.resume_skills = resume_skills
        if resume_skills:
            st.write(", ".join(resume_skills))
        else:
            st.warning("No known skills found. Add more to taxonomy in /data/skills_taxonomy.json")
    else:
        st.info("Upload a resume to start.")

    st.subheader("Proficiency Estimates")
    prof_map = {}
    for sk in st.session_state.resume_skills:
        scores = proficiency_score(st.session_state.resume_text, sk)
        prof_map[sk] = {**scores, "level": level_from_scores(scores)}
    st.session_state.proficiency = prof_map

    if prof_map:
        cols = st.columns(3)
        i = 0
        for sk, sc in prof_map.items():
            with cols[i % 3]:
                st.metric(
                    sk,
                    sc["level"].title(),
                    help=f"Beginner: {sc['beginner']:.2f}, Intermediate: {sc['intermediate']:.2f}, Advanced: {sc['advanced']:.2f}"
                )
            i += 1

    if st.session_state.job_desc and st.session_state.resume_skills:
        st.subheader("Job Match & Skill Gaps")
        common, missing = compare_with_job_desc(
            st.session_state.resume_skills,
            st.session_state.job_desc,
            all_skills
        )
        st.success(f"Overlap with JD: {', '.join(common) if common else 'None'}")
        st.error(f"Missing vs JD: {', '.join(missing) if missing else 'None'}")

# ... (keep the `with tab2:` block as is) ...
with tab2:
    st.markdown("""
### What's Next?

**Use the sidebar navigation to explore the other tools:**

-   **🧠 Skills & Proficiency** — A detailed, visual breakdown of your skills.
-   **🎯 Adaptive Questions** — Begin a simulated, timed interview based on your skills.
-   **📊 Evaluation & Recommendations** — Get feedback on your interview answers.
-   **🗺️ Learning Roadmap** — Get a personalized plan to fill your skill gaps.
-   **📝 Technical Assessment** — Generate a multiple-choice quiz to test your knowledge.
-   **✨ Resume Optimizer** — Use AI to rewrite and improve your resume bullet points.
-   **💬 Behavioral Coach** — Prepare for soft-skill questions based on the job description.
-   **🔬 Skill Deep Dive** — An ML feature to see real-world examples of skill progression.
-   **💡 Contribution Analysis** — A custom ML model to evaluate the impact of each skill on your ATS score.
""")