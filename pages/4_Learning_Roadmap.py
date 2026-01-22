import streamlit as st
import os
from utils.roadmap import load_learning_resources, generate_learning_roadmap
from utils.skills import compare_with_job_desc

st.set_page_config(page_title="Learning Roadmap", page_icon="🗺️", layout="wide")
st.title("🗺️ Personalized Learning Roadmap")

# Check for necessary session state variables
if "job_desc" not in st.session_state or not st.session_state.job_desc:
    st.warning("To generate a learning roadmap, please go to the main page and paste a Job Description.")
    st.stop()

if "resume_skills" not in st.session_state:
    st.warning("Please upload and process a resume on the main page first.")
    st.stop()

# --- Load Data ---
RESOURCES_PATH = os.path.join("data", "learning_resources.json")
learning_resources = load_learning_resources(RESOURCES_PATH)

if not learning_resources:
    st.error("Could not load learning resources. Make sure `data/learning_resources.json` exists.")
    st.stop()

# --- Identify Skill Gaps ---
# This re-calculates the gaps, which is fine. It ensures the page can run independently.
resume_skills = st.session_state.get("resume_skills", [])
job_desc = st.session_state.get("job_desc", "")
all_skills = st.session_state.get("all_skills", [])

common_skills, missing_skills = compare_with_job_desc(
    resume_skills,
    job_desc,
    all_skills
)

st.info(f"This roadmap is based on the **{len(missing_skills)} skills** identified as gaps between your resume and the job description.")

# --- Generate and Display Roadmap ---
if not missing_skills:
    st.success("Great news! No significant skill gaps were found based on the job description provided. Your resume seems to be a strong match.")
else:
    roadmap = generate_learning_roadmap(missing_skills, learning_resources)
    
    if not roadmap:
        st.warning("No learning resources found for the identified skill gaps. The skills might be too niche or need to be added to `data/learning_resources.json`.")
    else:
        st.header("Your Recommended Learning Plan")
        
        # Sort skills for consistent ordering
        sorted_skills = sorted(roadmap.keys())
        
        for skill in sorted_skills:
            with st.expander(f"**Learn {skill}**"):
                st.markdown(f"Here are some resources to help you master **{skill}**:")
                
                resources = roadmap[skill]
                for res in resources:
                    st.markdown(
                        f"- **[{res['title']}]({res['url']})** ({res.get('type', 'Resource')}) - *Difficulty: {res.get('difficulty', 'N/A')}*"
                    )

# Add a section for skills without resources
skills_with_no_resources = [s for s in missing_skills if s not in roadmap]
if skills_with_no_resources:
    st.subheader("Skills to Research Further")
    st.warning(f"We don't have specific learning resources for the following skills yet. We recommend searching for tutorials on platforms like YouTube, Udemy, or official documentation:")
    st.write("- " + "\n- ".join(sorted(skills_with_no_resources)))