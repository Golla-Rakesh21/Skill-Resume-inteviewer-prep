# import streamlit as st
# from utils.questions import generate_questions

# st.set_page_config(page_title="Adaptive Questions", page_icon="🎯", layout="wide")

# st.title("🎯 Adaptive Question Generation")

# # Load extracted skills & proficiencies from resume
# skills = st.session_state.get("resume_skills", [])
# prof = st.session_state.get("proficiency", {})

# if not skills:
#     st.warning("No skills found. Go back to the main page and upload a resume.")
#     st.stop()

# st.write("Select one or more skills and generate tailored questions.")
# selected = st.multiselect("Skills", skills, default=skills[:1])

# # Map difficulty levels for selected skills
# difficulty_map = {sk: prof.get(sk, {}).get("level", "beginner") for sk in selected}

# # Slider for number of questions
# n = st.slider("Questions per skill", 1, 8, 5)

# # Generate questions
# if st.button("Generate Questions"):
#     all_qs = {}
#     for sk in selected:
#         level = difficulty_map.get(sk, "beginner")
#         qs = generate_questions(sk, level, n=n)
#         all_qs[sk] = qs
#     st.session_state["generated_questions"] = all_qs

# # Display questions with answer boxes
# if "generated_questions" in st.session_state:
#     st.subheader("Questions")
#     for sk, qs in st.session_state["generated_questions"].items():
#         st.markdown(f"### {sk} ({difficulty_map.get(sk,'beginner').title()})")
#         for i, q in enumerate(qs, start=1):
#             with st.expander(f"Q{i}: {q}"):
#                 ans_key = f"ans_{sk}_{i}"  # unique key for each answer
#                 st.text_area(
#                      "Your answer",
#                      key=ans_key,   # Streamlit auto-stores text here
#                     height=150
#                 )


# pages/2_Questions.py
# import streamlit as st
# from utils.questions import generate_questions

# st.set_page_config(page_title="Adaptive Questions", page_icon="🎯", layout="wide")

# st.title("🎯 Adaptive Question Generation")

# # Load extracted skills & proficiencies from resume
# skills = st.session_state.get("resume_skills", [])
# prof = st.session_state.get("proficiency", {})

# if not skills:
#     st.warning("No skills found. Go back to the main page and upload a resume.")
#     st.stop()

# st.write("Select one or more skills and generate tailored questions.")
# selected = st.multiselect("Skills", skills, default=skills[:1])

# # Map difficulty levels for selected skills
# difficulty_map = {sk: prof.get(sk, {}).get("level", "beginner") for sk in selected}

# # Slider for number of questions
# n = st.slider("Questions per skill", 1, 8, 3) # Changed default to 3 for quicker testing

# # Initialize a structure to hold questions AND answers
# if "generated_qa" not in st.session_state:
#     st.session_state["generated_qa"] = {} # Will store {'skill': [{'q': question_str, 'a': answer_str}]}

# if st.button("Generate Questions"):
#     st.session_state["generated_qa"] = {} # Reset for new generation
#     for sk in selected:
#         level = difficulty_map.get(sk, "beginner")
#         qs = generate_questions(sk, level, n=n)
#         # Store questions with empty answers initially
#         st.session_state["generated_qa"][sk] = [{'q': q_text, 'a': ''} for q_text in qs]
#     st.success("Questions generated!")

# # Display questions with answer boxes
# if "generated_qa" in st.session_state and st.session_state["generated_qa"]:
#     st.subheader("Questions")
#     # Using a form to capture all answers at once, or rely on text_area's key behavior
#     # Let's stick with text_area's key for now, but manage state more explicitly

#     # This dictionary will temporarily hold user input for answers on this page run
#     current_answers = {} 

#     for sk, qa_list in st.session_state["generated_qa"].items():
#         st.markdown(f"### {sk} ({difficulty_map.get(sk,'beginner').title()})")
#         for i, qa_item in enumerate(qa_list, start=1):
#             q = qa_item['q']
#             # Use a unique key for each text area
#             ans_key = f"answer_for_{sk}_{i}" 
            
#             # Retrieve the current answer from session state or default to empty
#             # If the user has typed, st.text_area with key will update st.session_state automatically
#             current_answer_text = st.session_state.get(ans_key, qa_item['a']) 
            
#             user_input = st.text_area(
#                  f"Your answer for Q{i}: {q}",
#                  value=current_answer_text, # Set initial value from session state
#                  key=ans_key,               # Streamlit auto-stores text here
#                  height=150
#             )
#             # Crucially, update the 'a' field in the session_state['generated_qa'] structure
#             # This ensures that when the user types, the answer is immediately associated
#             # with the question in our primary data structure.
#             st.session_state["generated_qa"][sk][i-1]['a'] = user_input

#     st.info("Your answers are automatically saved. Navigate to '3_Evaluation_and_Recommendations' to see your scores.")



# import streamlit as st
# import time
# from utils.questions import generate_questions

# st.set_page_config(page_title="Adaptive Questions", page_icon="🎯", layout="wide")

# st.title("🎯 Adaptive Question Generation & Interview Simulation")

# # Load extracted skills & proficiencies from resume
# skills = st.session_state.get("resume_skills", [])
# prof = st.session_state.get("proficiency", {})

# if not skills:
#     st.warning("No skills found. Go back to the main page and upload a resume.")
#     st.stop()

# st.write("Select one or more skills and generate tailored questions.")
# selected = st.multiselect("Skills", skills, default=skills[:1])

# # Map difficulty levels for selected skills
# difficulty_map = {sk: prof.get(sk, {}).get("level", "beginner") for sk in selected}

# # Slider for number of questions
# n = st.slider("Questions per skill", 1, 8, 3) # Default to 3 for quicker testing

# # Initialize a structure to hold questions AND answers
# if "generated_qa" not in st.session_state:
#     st.session_state["generated_qa"] = {} # Will store {'skill': [{'q': question_str, 'a': answer_str}]}

# # --- Timer and Interview State Management ---
# if "interview_started" not in st.session_state:
#     st.session_state.interview_started = False
# if "current_question_index" not in st.session_state:
#     st.session_state.current_question_index = 0
# if "start_time" not in st.session_state:
#     st.session_state.start_time = 0
# if "question_start_time" not in st.session_state:
#     st.session_state.question_start_time = 0
# if "question_timers" not in st.session_state:
#     st.session_state.question_timers = {} # Store time spent per question: {(skill, index): time_spent}
# if "total_questions_list" not in st.session_state:
#     st.session_state.total_questions_list = [] # Flattened list of (skill, q_index) tuples

# QUESTION_TIME_LIMIT_SECONDS = st.slider("Time limit per question (seconds)", 30, 300, 180) # Default 3 minutes


# # Button to generate questions
# if st.button("Generate Questions for Interview Simulation"):
#     st.session_state["generated_qa"] = {} # Reset for new generation
#     st.session_state.total_questions_list = [] # Reset flattened list

#     for sk in selected:
#         level = difficulty_map.get(sk, "beginner")
#         qs = generate_questions(sk, level, n=n)
#         st.session_state["generated_qa"][sk] = [{'q': q_text, 'a': ''} for q_text in qs]
#         for i in range(len(qs)):
#             st.session_state.total_questions_list.append((sk, i))

#     st.session_state.interview_started = False # Reset interview state
#     st.session_state.current_question_index = 0
#     st.session_state.start_time = 0
#     st.session_state.question_start_time = 0
#     st.session_state.question_timers = {}
#     st.success("Questions generated! Click 'Start Interview' to begin.")


# # --- Interview Flow ---
# if st.session_state["generated_qa"]:
#     # Flatten the questions for sequential display
#     all_questions_flat = []
#     for sk, qa_list in st.session_state["generated_qa"].items():
#         for i, qa_item in enumerate(qa_list):
#             all_questions_flat.append({'skill': sk, 'q_index': i, 'question': qa_item['q']})

#     total_questions = len(all_questions_flat)

#     if not st.session_state.interview_started:
#         if st.button("Start Interview"):
#             st.session_state.interview_started = True
#             st.session_state.current_question_index = 0
#             st.session_state.start_time = time.time()
#             st.session_state.question_start_time = time.time() # Start timer for first question
#             st.rerun() # Rerun to start interview display
#     else:
#         # Display current question
#         current_idx = st.session_state.current_question_index
#         if current_idx < total_questions:
#             current_qa_item = all_questions_flat[current_idx]
#             current_skill = current_qa_item['skill']
#             current_q_text = current_qa_item['question']
#             original_q_index = current_qa_item['q_index'] # 0-indexed original position within skill

#             st.markdown(f"### Question {current_idx + 1} of {total_questions} ({current_skill} - {difficulty_map.get(current_skill,'beginner').title()})")
#             st.write(f"**Q:** {current_q_text}")

#             # Timer display
#             timer_placeholder = st.empty()
#             time_elapsed_q = int(time.time() - st.session_state.question_start_time)
#             remaining_time = QUESTION_TIME_LIMIT_SECONDS - time_elapsed_q

#             if remaining_time <= 0:
#                 timer_placeholder.error(f"Time's up for this question! ({QUESTION_TIME_LIMIT_SECONDS} seconds)")
#                 # Automatically save whatever is in the text_area at time's up
#                 ans_key = f"answer_for_{current_skill}_{original_q_index}"
#                 current_answer_text = st.session_state.get(ans_key, "")
#                 st.session_state["generated_qa"][current_skill][original_q_index]['a'] = current_answer_text

#                 # Store time spent
#                 st.session_state.question_timers[(current_skill, original_q_index)] = QUESTION_TIME_LIMIT_SECONDS

#                 # Auto-advance to next question
#                 st.session_state.current_question_index += 1
#                 if st.session_state.current_question_index < total_questions:
#                     st.session_state.question_start_time = time.time() # Start timer for next question
#                 st.rerun()
#             else:
#                 timer_placeholder.info(f"Time remaining: {remaining_time} seconds")

#             # Answer input
#             ans_key = f"answer_for_{current_skill}_{original_q_index}"
#             # Retrieve current answer from our generated_qa structure for persistent display
#             initial_answer_text = st.session_state["generated_qa"][current_skill][original_q_index]['a']

#             user_input = st.text_area(
#                  "Your answer",
#                  value=initial_answer_text, # Set initial value from session state
#                  key=ans_key,               # Streamlit auto-stores text here
#                  height=150
#             )
#             # Crucially, update the 'a' field in the session_state['generated_qa'] structure
#             st.session_state["generated_qa"][current_skill][original_q_index]['a'] = user_input

#             col_prev, col_next = st.columns(2)
#             with col_prev:
#                 if st.button("Previous Question", disabled=(current_idx == 0)):
#                     # Save current answer before moving
#                     st.session_state["generated_qa"][current_skill][original_q_index]['a'] = user_input
#                     # Store time spent for current question
#                     st.session_state.question_timers[(current_skill, original_q_index)] = time_elapsed_q
                    
#                     st.session_state.current_question_index -= 1
#                     # Restart timer for new current question (if it existed before)
#                     prev_qa_item = all_questions_flat[st.session_state.current_question_index]
#                     prev_skill = prev_qa_item['skill']
#                     prev_original_q_index = prev_qa_item['q_index']
#                     # Restore previous question's elapsed time if available, otherwise start fresh
#                     st.session_state.question_start_time = time.time() - st.session_state.question_timers.get((prev_skill, prev_original_q_index), 0)
#                     st.rerun()
#             with col_next:
#                 if st.button("Next Question", disabled=(current_idx == total_questions - 1)):
#                     # Save current answer before moving
#                     st.session_state["generated_qa"][current_skill][original_q_index]['a'] = user_input
#                     # Store time spent for current question
#                     st.session_state.question_timers[(current_skill, original_q_index)] = time_elapsed_q
                    
#                     st.session_state.current_question_index += 1
#                     if st.session_state.current_question_index < total_questions:
#                         st.session_state.question_start_time = time.time() # Start timer for next question
#                     st.rerun()

#             # Rerun the script every second to update the timer
#             time.sleep(1)
#             st.rerun() # This keeps the timer ticking
#         else:
#             st.success("Interview finished! Go to '3_Evaluation_and_Recommendations' for your full report.")
#             st.session_state.interview_started = False # Mark interview as finished
#             # Finalize total time
#             total_interview_time = int(time.time() - st.session_state.start_time)
#             st.session_state.total_interview_time = total_interview_time
# else:
#     st.info("Generate questions to start your interview simulation.")




import streamlit as st
import time
from utils.questions import generate_questions

st.set_page_config(page_title="Adaptive Questions", page_icon="🎯", layout="wide")

st.title("🎯 Adaptive Question Generation & Interview Simulation")

# Load extracted skills & proficiencies from resume
skills = st.session_state.get("resume_skills", [])
prof = st.session_state.get("proficiency", {})

if not skills:
    st.warning("No skills found. Go back to the main page and upload a resume.")
    st.stop()

st.write("Select one or more skills and generate tailored questions.")
selected = st.multiselect("Skills", skills, default=skills[:1])

# Map difficulty levels for selected skills
difficulty_map = {sk: prof.get(sk, {}).get("level", "beginner") for sk in selected}

# Slider for number of questions
n = st.slider("Questions per skill", 1, 8, 3) # Default to 3 for quicker testing

# Initialize a structure to hold questions AND answers
if "generated_qa" not in st.session_state:
    st.session_state["generated_qa"] = {} # Will store {'skill': [{'q': question_str, 'a': answer_str}]}

# --- Timer and Interview State Management ---
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = 0
if "question_timers" not in st.session_state:
    st.session_state.question_timers = {} # Store time spent per question: {(skill, index): time_spent}
if "total_questions_list" not in st.session_state:
    st.session_state.total_questions_list = [] # Flattened list of (skill, q_index) tuples

QUESTION_TIME_LIMIT_SECONDS = st.slider("Time limit per question (seconds)", 30, 300, 180) # Default 3 minutes


# Button to generate questions
if st.button("Generate Questions for Interview Simulation"):
    st.session_state["generated_qa"] = {} # Reset for new generation
    st.session_state.total_questions_list = [] # Reset flattened list

    for sk in selected:
        level = difficulty_map.get(sk, "beginner")
        qs = generate_questions(sk, level, n=n)
        st.session_state["generated_qa"][sk] = [{'q': q_text, 'a': ''} for q_text in qs]
        for i in range(len(qs)):
            st.session_state.total_questions_list.append((sk, i))

    st.session_state.interview_started = False # Reset interview state
    st.session_state.current_question_index = 0
    st.session_state.start_time = 0
    st.session_state.question_start_time = 0
    st.session_state.question_timers = {}
    st.success("Questions generated! Click 'Start Interview' to begin.")


# --- Interview Flow ---
if st.session_state["generated_qa"]:
    # Flatten the questions for sequential display
    all_questions_flat = []
    for sk, qa_list in st.session_state["generated_qa"].items():
        for i, qa_item in enumerate(qa_list):
            all_questions_flat.append({'skill': sk, 'q_index': i, 'question': qa_item['q']})

    total_questions = len(all_questions_flat)

    if not st.session_state.interview_started:
        if st.button("Start Interview"):
            st.session_state.interview_started = True
            st.session_state.current_question_index = 0
            st.session_state.start_time = time.time()
            st.session_state.question_start_time = time.time() # Start timer for first question
            st.rerun() # Rerun to start interview display
    else:
        # Display current question
        current_idx = st.session_state.current_question_index
        if current_idx < total_questions:
            current_qa_item = all_questions_flat[current_idx]
            current_skill = current_qa_item['skill']
            current_q_text = current_qa_item['question']
            original_q_index = current_qa_item['q_index'] # 0-indexed original position within skill

            st.markdown(f"### Question {current_idx + 1} of {total_questions} ({current_skill} - {difficulty_map.get(current_skill,'beginner').title()})")
            st.write(f"**Q:** {current_q_text}")

            # Timer display
            timer_placeholder = st.empty()
            time_elapsed_q = int(time.time() - st.session_state.question_start_time)
            remaining_time = QUESTION_TIME_LIMIT_SECONDS - time_elapsed_q

            if remaining_time <= 0:
                timer_placeholder.error(f"Time's up for this question! ({QUESTION_TIME_LIMIT_SECONDS} seconds)")
                # Automatically save whatever is in the text_area at time's up
                ans_key = f"answer_for_{current_skill}_{original_q_index}"
                current_answer_text = st.session_state.get(ans_key, "")
                st.session_state["generated_qa"][current_skill][original_q_index]['a'] = current_answer_text

                # Store time spent
                st.session_state.question_timers[(current_skill, original_q_index)] = QUESTION_TIME_LIMIT_SECONDS

                # Auto-advance to next question
                st.session_state.current_question_index += 1
                if st.session_state.current_question_index < total_questions:
                    st.session_state.question_start_time = time.time() # Start timer for next question
                st.rerun()
            else:
                timer_placeholder.info(f"Time remaining: {remaining_time} seconds")

            # Answer input
            ans_key = f"answer_for_{current_skill}_{original_q_index}"
            # Retrieve current answer from our generated_qa structure for persistent display
            initial_answer_text = st.session_state["generated_qa"][current_skill][original_q_index]['a']

            user_input = st.text_area(
                 "Your answer",
                 value=initial_answer_text, # Set initial value from session state
                 key=ans_key,               # Streamlit auto-stores text here
                 height=150
            )
            # Crucially, update the 'a' field in the session_state['generated_qa'] structure
            st.session_state["generated_qa"][current_skill][original_q_index]['a'] = user_input

            col_prev, col_next = st.columns(2)
            with col_prev:
                if st.button("Previous Question", disabled=(current_idx == 0)):
                    # Save current answer before moving
                    st.session_state["generated_qa"][current_skill][original_q_index]['a'] = user_input
                    # Store time spent for current question
                    st.session_state.question_timers[(current_skill, original_q_index)] = time_elapsed_q
                    
                    st.session_state.current_question_index -= 1
                    # Restart timer for new current question (if it existed before)
                    prev_qa_item = all_questions_flat[st.session_state.current_question_index]
                    prev_skill = prev_qa_item['skill']
                    prev_original_q_index = prev_qa_item['q_index']
                    # Restore previous question's elapsed time if available, otherwise start fresh
                    st.session_state.question_start_time = time.time() - st.session_state.question_timers.get((prev_skill, prev_original_q_index), 0)
                    st.rerun()
            with col_next:
                if st.button("Next Question", disabled=(current_idx == total_questions - 1)):
                    # Save current answer before moving
                    st.session_state["generated_qa"][current_skill][original_q_index]['a'] = user_input
                    # Store time spent for current question
                    st.session_state.question_timers[(current_skill, original_q_index)] = time_elapsed_q
                    
                    st.session_state.current_question_index += 1
                    if st.session_state.current_question_index < total_questions:
                        st.session_state.question_start_time = time.time() # Start timer for next question
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True) # Add some space
            if st.button("Submit Interview & Finish Early", type="primary"):
                # Save the final answer before submitting
                st.session_state["generated_qa"][current_skill][original_q_index]['a'] = user_input
                
                # Store time spent for the final question
                time_elapsed_q = int(time.time() - st.session_state.question_start_time)
                st.session_state.question_timers[(current_skill, original_q_index)] = time_elapsed_q
                
                # Set the index to the end to trigger the "finished" state on the next run
                st.session_state.current_question_index = total_questions
                
                st.rerun()

            # Rerun the script every second to update the timer
            time.sleep(1)
            st.rerun() # This keeps the timer ticking
        else:
            st.success("Interview finished! Go to '3_Evaluation_and_Recommendations' for your full report.")
            st.session_state.interview_started = False # Mark interview as finished
            # Finalize total time
            if "total_interview_time" not in st.session_state:
                total_interview_time = int(time.time() - st.session_state.start_time)
                st.session_state.total_interview_time = total_interview_time
else:
    st.info("Generate questions to start your interview simulation.")