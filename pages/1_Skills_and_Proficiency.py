# import streamlit as st
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import os # Import os for TAXO_PATH
# from utils.skills import load_taxonomy, build_skill_index # Import these to ensure full context

# st.set_page_config(page_title="Skills & Proficiency", page_icon="🧠", layout="wide")
# st.title("🧠 Skills & Proficiency")
# st.write("This information is shown on the main page. Use sidebar there to (re)upload resume and JD.")
# st.info("Tip: Edit data/skills_taxonomy.json to add more skills for your domain.")

# # Re-load taxonomy and all_skills if not already in session state or to ensure consistency
# # (These are typically loaded in app.py, but good to ensure availability here if this page is directly accessed)
# if "taxonomy" not in st.session_state:
#     TAXO_PATH = os.path.join("data", "skills_taxonomy.json")
#     st.session_state.taxonomy = load_taxonomy(TAXO_PATH)
# if "all_skills" not in st.session_state:
#     st.session_state.all_skills = build_skill_index(st.session_state.taxonomy)


# # --- Existing Code for displaying individual metrics ---
# st.subheader("Extracted Skills")
# if st.session_state.resume_text:
#     # Ensure resume_skills are up-to-date (they should be set in app.py after upload)
#     if not st.session_state.resume_skills:
#         st.session_state.resume_skills = [] # Initialize if somehow empty
#     if st.session_state.resume_skills:
#         st.write(", ".join(st.session_state.resume_skills))
#     else:
#         st.warning("No known skills found. Add more to taxonomy in /data/skills_taxonomy.json")
# else:
#     st.info("Upload a resume to start.")

# st.subheader("Proficiency Estimates")
# prof_map = st.session_state.get("proficiency", {}) # Get from session state

# if prof_map:
#     cols = st.columns(3)
#     i = 0
#     for sk, sc in prof_map.items():
#         with cols[i % 3]:
#             st.metric(
#                 sk,
#                 sc["level"].title(),
#                 help=f"Beginner: {sc['beginner']:.2f}, Intermediate: {sc['intermediate']:.2f}, Advanced: {sc['advanced']:.2f}"
#             )
#         i += 1

#     # --- New Code for Visualization ---
#     st.subheader("Skill Proficiency Visualization")

#     # Prepare data for plotting
#     skills_for_plot = list(prof_map.keys())
#     if not skills_for_plot:
#         st.info("No skills to visualize yet.")
#     else:
#         beginner_scores = [prof_map[sk]["beginner"] for sk in skills_for_plot]
#         intermediate_scores = [prof_map[sk]["intermediate"] for sk in skills_for_plot]
#         advanced_scores = [prof_map[sk]["advanced"] for sk in skills_for_plot]

#         # Create a DataFrame for easier plotting (especially for bar charts)
#         plot_df = pd.DataFrame({
#             'Skill': skills_for_plot,
#             'Beginner': beginner_scores,
#             'Intermediate': intermediate_scores,
#             'Advanced': advanced_scores
#         }).set_index('Skill')

#         # Option 1: Stacked Bar Chart (often clearer than radar for many items)
#         st.write("#### Stacked Bar Chart")
#         fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
#         plot_df[['Beginner', 'Intermediate', 'Advanced']].plot(
#             kind='bar',
#             stacked=True,
#             color=['#ADD8E6', '#FFD700', '#FF4500'], # LightBlue, Gold, OrangeRed
#             ax=ax_bar
#         )
#         ax_bar.set_title('Skill Proficiency Levels')
#         ax_bar.set_ylabel('Proficiency Score (Normalized)')
#         ax_bar.set_xticklabels(skills_for_plot, rotation=45, ha='right')
#         ax_bar.legend(title='Level')
#         plt.tight_layout()
#         st.pyplot(fig_bar)
#         plt.close(fig_bar) # Close the figure to free memory

#         # Option 2: Radar Chart (Spider Chart) - better for fewer skills
#         st.write("#### Radar Chart (Best for a few skills)")
#         if len(skills_for_plot) > 1: # Radar chart needs at least 2 skills
#             categories = ['Beginner', 'Intermediate', 'Advanced']
#             num_vars = len(categories)

#             # Define angle for each axis
#             angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
#             angles += angles[:1] # Complete the loop for plotting

#             fig_radar, ax_radar = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

#             # Loop through each skill to plot its radar
#             for sk_idx, skill_name in enumerate(skills_for_plot):
#                 # We need scores for each category
#                 values = [
#                     plot_df.loc[skill_name, 'Beginner'],
#                     plot_df.loc[skill_name, 'Intermediate'],
#                     plot_df.loc[skill_name, 'Advanced']
#                 ]
#                 values += values[:1] # Complete the loop for plotting

#                 ax_radar.plot(angles, values, linewidth=1, linestyle='solid', label=skill_name)
#                 ax_radar.fill(angles, values, alpha=0.25)

#             ax_radar.set_theta_offset(np.pi / 2)
#             ax_radar.set_theta_direction(-1)
#             ax_radar.set_rlabel_position(0)
#             ax_radar.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
#             ax_radar.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], color="grey", size=7)
#             ax_radar.set_ylim(0, 1)
#             ax_radar.set_xticks(angles[:-1])
#             ax_radar.set_xticklabels(categories)
#             ax_radar.set_title("Skill Proficiency Radar", va='bottom')
#             ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
#             plt.tight_layout()
#             st.pyplot(fig_radar)
#             plt.close(fig_radar) # Close the figure to free memory
#         elif len(skills_for_plot) == 1:
#             st.info(f"Radar chart needs at least two skills for comparison. Displaying scores for '{skills_for_plot[0]}' only above.")


#     # --- Existing Code for Job Match & Skill Gaps ---
#     if st.session_state.get("job_desc") and st.session_state.resume_skills: # Use .get for safety
#         st.subheader("Job Match & Skill Gaps")
#         common, missing = compare_with_job_desc(
#             st.session_state.resume_skills,
#             st.session_state.job_desc,
#             st.session_state.all_skills # Use from session state
#         )
#         st.success(f"Overlap with JD: {', '.join(common) if common else 'None'}")
#         st.error(f"Missing vs JD: {', '.join(missing) if missing else 'None'}")
# else:
#     st.info("Upload a resume to see proficiency estimates and visualizations.")


import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os # Import os for TAXO_PATH
from utils.skills import load_taxonomy, build_skill_index, compare_with_job_desc # Import these to ensure full context

st.set_page_config(page_title="Skills & Proficiency", page_icon="🧠", layout="wide")
st.title("🧠 Skills & Proficiency")
st.write("This information is shown on the main page. Use sidebar there to (re)upload resume and JD.")
st.info("Tip: Edit data/skills_taxonomy.json to add more skills for your domain.")

# Re-load taxonomy and all_skills if not already in session state or to ensure consistency
# (These are typically loaded in app.py, but good to ensure availability here if this page is directly accessed)
if "taxonomy" not in st.session_state:
    TAXO_PATH = os.path.join("data", "skills_taxonomy.json")
    st.session_state.taxonomy = load_taxonomy(TAXO_PATH)
if "all_skills" not in st.session_state:
    st.session_state.all_skills = build_skill_index(st.session_state.taxonomy)


# --- Existing Code for displaying individual metrics ---
st.subheader("Extracted Skills")
if st.session_state.resume_text:
    # Ensure resume_skills are up-to-date (they should be set in app.py after upload)
    if not st.session_state.resume_skills:
        st.session_state.resume_skills = [] # Initialize if somehow empty
    if st.session_state.resume_skills:
        st.write(", ".join(st.session_state.resume_skills))
    else:
        st.warning("No known skills found. Add more to taxonomy in /data/skills_taxonomy.json")
else:
    st.info("Upload a resume to start.")

st.subheader("Proficiency Estimates")
prof_map = st.session_state.get("proficiency", {}) # Get from session state

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

    # --- New Code for Visualization ---
    st.subheader("Skill Proficiency Visualization")

    # Prepare data for plotting
    skills_for_plot = list(prof_map.keys())
    if not skills_for_plot:
        st.info("No skills to visualize yet.")
    else:
        beginner_scores = [prof_map[sk]["beginner"] for sk in skills_for_plot]
        intermediate_scores = [prof_map[sk]["intermediate"] for sk in skills_for_plot]
        advanced_scores = [prof_map[sk]["advanced"] for sk in skills_for_plot]

        # Create a DataFrame for easier plotting (especially for bar charts)
        plot_df = pd.DataFrame({
            'Skill': skills_for_plot,
            'Beginner': beginner_scores,
            'Intermediate': intermediate_scores,
            'Advanced': advanced_scores
        }).set_index('Skill')

        # Option 1: Stacked Bar Chart (often clearer than radar for many items)
        st.write("#### Stacked Bar Chart")
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        plot_df[['Beginner', 'Intermediate', 'Advanced']].plot(
            kind='bar',
            stacked=True,
            color=['#ADD8E6', '#FFD700', '#FF4500'], # LightBlue, Gold, OrangeRed
            ax=ax_bar
        )
        ax_bar.set_title('Skill Proficiency Levels')
        ax_bar.set_ylabel('Proficiency Score (Normalized)')
        ax_bar.set_xticklabels(skills_for_plot, rotation=45, ha='right')
        ax_bar.legend(title='Level')
        plt.tight_layout()
        st.pyplot(fig_bar)
        plt.close(fig_bar) # Close the figure to free memory

        # Option 2: Radar Chart (Spider Chart) - better for fewer skills
        st.write("#### Radar Chart (Best for a few skills)")
        if len(skills_for_plot) > 1: # Radar chart needs at least 2 skills
            categories = ['Beginner', 'Intermediate', 'Advanced']
            num_vars = len(categories)

            # Define angle for each axis
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            angles += angles[:1] # Complete the loop for plotting

            fig_radar, ax_radar = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

            # Loop through each skill to plot its radar
            for sk_idx, skill_name in enumerate(skills_for_plot):
                # We need scores for each category
                values = [
                    plot_df.loc[skill_name, 'Beginner'],
                    plot_df.loc[skill_name, 'Intermediate'],
                    plot_df.loc[skill_name, 'Advanced']
                ]
                values += values[:1] # Complete the loop for plotting

                ax_radar.plot(angles, values, linewidth=1, linestyle='solid', label=skill_name)
                ax_radar.fill(angles, values, alpha=0.25)

            ax_radar.set_theta_offset(np.pi / 2)
            ax_radar.set_theta_direction(-1)
            ax_radar.set_rlabel_position(0)
            ax_radar.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
            ax_radar.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], color="grey", size=7)
            ax_radar.set_ylim(0, 1)
            ax_radar.set_xticks(angles[:-1])
            ax_radar.set_xticklabels(categories)
            ax_radar.set_title("Skill Proficiency Radar", va='bottom')
            ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            plt.tight_layout()
            st.pyplot(fig_radar)
            plt.close(fig_radar) # Close the figure to free memory
        elif len(skills_for_plot) == 1:
            st.info(f"Radar chart needs at least two skills for comparison. Displaying scores for '{skills_for_plot[0]}' only above.")


    # --- Existing Code for Job Match & Skill Gaps ---
    if st.session_state.get("job_desc") and st.session_state.resume_skills: # Use .get for safety
        st.subheader("Job Match & Skill Gaps")
        common, missing = compare_with_job_desc(
            st.session_state.resume_skills,
            st.session_state.job_desc,
            st.session_state.all_skills # Use from session state
        )
        st.success(f"Overlap with JD: {', '.join(common) if common else 'None'}")
        st.error(f"Missing vs JD: {', '.join(missing) if missing else 'None'}")
else:
    st.info("Upload a resume to see proficiency estimates and visualizations.")


    