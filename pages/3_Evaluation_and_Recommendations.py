# # 3_Evaluation.py
# import streamlit as st
# import pandas as pd
# from utils.evaluator import evaluate_answer
# from utils.skills import load_taxonomy, build_skill_index

# st.set_page_config(page_title="Evaluation & Recommendations", page_icon="📊", layout="wide")
# st.title("📊 Evaluation & Recommendations")

# # Retrieve generated questions
# # Ensure 'generated_questions' always exists as a dictionary
# if "generated_questions" not in st.session_state:
#     st.session_state.generated_questions = {}

# generated = st.session_state.generated_questions

# if not generated:
#     st.warning("No generated questions found. Go to '2_Questions' to create them first and answer them.")
#     st.stop()

# # Reference snippets per skill
# REFERENCE_SNIPPETS = {
#     "Python": [
#         "Python is a high-level, interpreted language used for scripting, data science, web, and automation.",
#         "Common Python tooling includes virtual environments, pip, pytest, and frameworks like Flask or Django.",
#         "Key features include dynamic typing, garbage collection, and extensive standard libraries.",
#         "Python is often used for web development (Django, Flask), data analysis (Pandas, NumPy), machine learning (Scikit-learn, TensorFlow), and automation."
#     ],
#     "React": [
#         "React is a front-end library based on components and a virtual DOM for efficient UI updates.",
#         "Production React apps emphasize state management (Context API, Redux), routing (React Router), code-splitting, and performance profiling.",
#         "Key concepts include JSX, props, state, lifecycle methods (or Hooks), and reconciliation.",
#         "React is used for building single-page applications (SPAs), complex user interfaces, and mobile apps (React Native)."
#     ],
#     "MongoDB": [
#         "MongoDB is a document database using BSON; common patterns include flexible schema design, indexing, and aggregations.",
#         "Production setups consider replica sets for high availability, sharding for horizontal scaling, backups, and monitoring.",
#         "It's a NoSQL database, offering high performance, high availability, and easy scalability.",
#         "Common operations include CRUD (Create, Read, Update, Delete), aggregation pipelines, and indexing for query optimization."
#     ],
#     "HTML": [
#         "HTML defines the structure of a web page using elements such as div, header, footer, and semantic tags (e.g., article, section, nav).",
#         "Performance bottlenecks in HTML can come from too many DOM nodes, blocking resources (scripts/stylesheets), or inline styles/scripts. Optimization involves minimizing DOM, deferring non-critical resources, and optimizing asset loading.",
#         "A production-ready HTML app emphasizes semantic markup for accessibility and SEO, responsive layout with viewports, and optimized asset delivery.",
#         "It uses tags to structure content like headings, paragraphs, lists, links, and images."
#     ],
#     "CSS": [
#         "CSS is used to style web pages, including layout, colors, fonts, and responsiveness.",
#         "Responsive design is achieved using media queries, Flexbox, and Grid for adaptable layouts across devices.",
#         "Common challenges include cross-browser compatibility, specificity conflicts (resolved by using BEM, CSS modules, or utility-first CSS), and maintaining modular and scalable styles.",
#         "It controls the visual presentation of HTML elements, including colors, fonts, spacing, and positioning."
#     ]
# }


# # Collect evaluations
# rows = []
# for sk, qs in generated.items():
#     for i, q in enumerate(qs, start=1):
#         ans_key = f"ans_{sk}_{i}"
#         # Retrieve the answer using the correct key from st.session_state
#         ans = st.session_state.get(ans_key, "").strip()

#         refs = REFERENCE_SNIPPETS.get(sk, [
#             "A strong answer explains core concepts, trade-offs, and production concerns."
#         ])

#         if ans:
#             eval_result = evaluate_answer(ans, refs)
#             score = eval_result["score"]
#             best_match = eval_result["best_match"]
#         else:
#             score = 0.0
#             best_match = ""

#         rows.append({
#             "Skill": sk,
#             "Q#": i,
#             "Question": q,
#             "Answer": ans if ans else "(not answered)",
#             "Score": score,
#             "Closest Reference": best_match
#         })

# df = pd.DataFrame(rows)

# # Show Q–A–Score table
# if not df.empty:
#     st.dataframe(df, use_container_width=True)
# else:
#     st.info("No questions have been answered yet.")

# # Average score metric
# avg = df["Score"].mean() if not df.empty else 0.0
# st.metric("Average Score", f"{avg:.1f}")

# # Load taxonomy & suggest next skills
# taxonomy = load_taxonomy("data/skills_taxonomy.json")
# all_skills = build_skill_index(taxonomy)
# resume_skills = st.session_state.get("resume_skills", [])

# NEXT_SKILL_SUGGESTIONS = {
#     "React": ["Next.js", "TypeScript", "Redux Toolkit", "GraphQL", "Jest", "Cypress"],
#     "Node.js": ["NestJS", "TypeScript", "Docker", "Microservices", "Kafka", "Redis"],
#     "Python": ["FastAPI", "PyTorch", "MLOps", "Django REST Framework", "Celery", "Pandas (Advanced)"],
#     "MongoDB": ["Mongoose", "Sharding", "Redis", "Elasticsearch", "Data Modeling (NoSQL)"],
#     "Docker": ["Kubernetes", "CI/CD", "Terraform", "Helm", "Prometheus", "Grafana"],
#     "HTML": ["Accessibility (WCAG)", "SEO Best Practices", "Web Performance Optimization", "PWA (Progressive Web Apps)", "Semantic HTML5"],
#     "CSS": ["Sass/Less", "Tailwind CSS", "CSS-in-JS (e.g., Styled Components)", "BEM Methodology", "CSS Grid Layout (Advanced)", "Animations"]
# }


# suggestions = []
# for s in resume_skills:
#     suggestions.extend(NEXT_SKILL_SUGGESTIONS.get(s, []))

# # Keep only new skills found in taxonomy
# suggestions = [s for s in suggestions if s in all_skills and s not in resume_skills]
# suggestions = sorted(set(suggestions))

# st.subheader("Suggested Next Skills")
# if suggestions:
#     st.write(", ".join(suggestions))
# else:
#     st.write("Based on your current skills, consider deepening knowledge in architecture, testing, and DevOps.")




# pages/3_Evaluation_and_Recommendations.py
# import streamlit as st
# import pandas as pd
# from utils.evaluator import evaluate_answer
# from utils.skills import load_taxonomy, build_skill_index

# st.set_page_config(page_title="Evaluation & Recommendations", page_icon="📊", layout="wide")
# st.title("📊 Evaluation & Recommendations")

# # Retrieve generated questions AND answers
# if "generated_qa" not in st.session_state or not st.session_state["generated_qa"]:
#     st.warning("No questions have been generated or answered yet. Go to '2_Questions' to create them first and provide your answers.")
#     st.stop()

# generated_qa = st.session_state["generated_qa"]

# # Reference snippets per skill (expanded for better scoring)
# REFERENCE_SNIPPETS = {
#     "Python": [
#         "Python is a high-level, interpreted language used for scripting, data science, web, and automation.",
#         "Common Python tooling includes virtual environments, pip, pytest, and frameworks like Flask or Django.",
#         "Key features include dynamic typing, garbage collection, and extensive standard libraries.",
#         "Python is often used for web development (Django, Flask), data analysis (Pandas, NumPy), machine learning (Scikit-learn, TensorFlow), and automation."
#     ],
#     "React": [
#         "React is a front-end library based on components and a virtual DOM for efficient UI updates.",
#         "Production React apps emphasize state management (Context API, Redux), routing (React Router), code-splitting, and performance profiling.",
#         "Key concepts include JSX, props, state, lifecycle methods (or Hooks), and reconciliation.",
#         "React is used for building single-page applications (SPAs), complex user interfaces, and mobile apps (React Native)."
#     ],
#     "MongoDB": [
#         "MongoDB is a document database using BSON; common patterns include flexible schema design, indexing, and aggregations.",
#         "Production setups consider replica sets for high availability, sharding for horizontal scaling, backups, and monitoring.",
#         "It's a NoSQL database, offering high performance, high availability, and easy scalability.",
#         "Common operations include CRUD (Create, Read, Update, Delete), aggregation pipelines, and indexing for query optimization."
#     ],
#     "HTML": [
#         "HTML defines the structure of a web page using elements such as div, header, footer, and semantic tags (e.g., article, section, nav).",
#         "Performance bottlenecks in HTML can come from too many DOM nodes, blocking resources (scripts/stylesheets), or inline styles/scripts. Optimization involves minimizing DOM, deferring non-critical resources, and optimizing asset loading.",
#         "A production-ready HTML app emphasizes semantic markup for accessibility and SEO, responsive layout with viewports, and optimized asset delivery.",
#         "It uses tags to structure content like headings, paragraphs, lists, links, and images."
#     ],
#     "CSS": [
#         "CSS is used to style web pages, including layout, colors, fonts, and responsiveness.",
#         "Responsive design is achieved using media queries, Flexbox, and Grid for adaptable layouts across devices.",
#         "Common challenges include cross-browser compatibility, specificity conflicts (resolved by using BEM, CSS modules, or utility-first CSS), and maintaining modular and scalable styles.",
#         "It controls the visual presentation of HTML elements, including colors, fonts, spacing, and positioning."
#     ]
# }


# # Collect evaluations
# rows = []
# total_answered_questions = 0
# for sk, qa_list in generated_qa.items():
#     for i, qa_item in enumerate(qa_list, start=1):
#         q = qa_item['q']
#         ans = qa_item['a'].strip() # Get the answer directly from our stored structure

#         refs = REFERENCE_SNIPPETS.get(sk, [
#             "A strong answer explains core concepts, trade-offs, and production concerns."
#         ])

#         if ans:
#             eval_result = evaluate_answer(ans, refs)
#             score = eval_result["score"]
#             best_match = eval_result["best_match"]
#             total_answered_questions += 1
#         else:
#             score = 0.0
#             best_match = ""

#         rows.append({
#             "Skill": sk,
#             "Q#": i,
#             "Question": q,
#             "Answer": ans if ans else "(not answered)",
#             "Score": score,
#             "Closest Reference": best_match
#         })

# df = pd.DataFrame(rows)

# # Show Q–A–Score table
# if not df.empty:
#     st.dataframe(df, width='stretch') # Updated to 'width' from 'use_container_width'
# else:
#     st.info("No questions have been answered yet.")

# # Average score metric
# # Calculate average only for questions that were actually answered
# avg = df[df["Answer"] != "(not answered)"]["Score"].mean() if not df[df["Answer"] != "(not answered)"].empty else 0.0
# st.metric("Average Score (of answered questions)", f"{avg:.1f}")


# # Load taxonomy & suggest next skills
# taxonomy = load_taxonomy("data/skills_taxonomy.json")
# all_skills = build_skill_index(taxonomy)
# resume_skills = st.session_state.get("resume_skills", [])

# NEXT_SKILL_SUGGESTIONS = {
#     "React": ["Next.js", "TypeScript", "Redux Toolkit", "GraphQL", "Jest", "Cypress"],
#     "Node.js": ["NestJS", "TypeScript", "Docker", "Microservices", "Kafka", "Redis"],
#     "Python": ["FastAPI", "PyTorch", "MLOps", "Django REST Framework", "Celery", "Pandas (Advanced)"],
#     "MongoDB": ["Mongoose", "Sharding", "Redis", "Elasticsearch", "Data Modeling (NoSQL)"],
#     "Docker": ["Kubernetes", "CI/CD", "Terraform", "Helm", "Prometheus", "Grafana"],
#     "HTML": ["Accessibility (WCAG)", "SEO Best Practices", "Web Performance Optimization", "PWA (Progressive Web Apps)", "Semantic HTML5"],
#     "CSS": ["Sass/Less", "Tailwind CSS", "CSS-in-JS (e.g., Styled Components)", "BEM Methodology", "CSS Grid Layout (Advanced)", "Animations"]
# }


# suggestions = []
# for s in resume_skills:
#     suggestions.extend(NEXT_SKILL_SUGGESTIONS.get(s, []))

# # Keep only new skills found in taxonomy
# suggestions = [s for s in suggestions if s in all_skills and s not in resume_skills]
# suggestions = sorted(set(suggestions))

# st.subheader("Suggested Next Skills")
# if suggestions:
#     st.write(", ".join(suggestions))
# else:
#     st.write("Based on your current skills, consider deepening knowledge in architecture, testing, and DevOps.")

# pages/3_Evaluation_and_Recommendations.py
import streamlit as st
import pandas as pd
from utils.evaluator import evaluate_answer
from utils.skills import load_taxonomy, build_skill_index

st.set_page_config(page_title="Evaluation & Recommendations", page_icon="📊", layout="wide")
st.title("📊 Evaluation & Recommendations")

# Retrieve generated questions AND answers
if "generated_qa" not in st.session_state or not st.session_state["generated_qa"]:
    st.warning("No questions have been generated or answered yet. Go to '2_Questions' to create them first and provide your answers.")
    st.stop()

generated_qa = st.session_state["generated_qa"]

# Reference snippets per skill (expanded for better scoring)
REFERENCE_SNIPPETS = {
    "Python": [
        "Python is a high-level, interpreted language used for scripting, data science, web, and automation.",
        "Common Python tooling includes virtual environments, pip, pytest, and frameworks like Flask or Django.",
        "Key features include dynamic typing, garbage collection, and extensive standard libraries.",
        "Python is often used for web development (Django, Flask), data analysis (Pandas, NumPy), machine learning (Scikit-learn, TensorFlow), and automation."
    ],
    "React": [
        "React is a front-end library based on components and a virtual DOM for efficient UI updates.",
        "Production React apps emphasize state management (Context API, Redux), routing (React Router), code-splitting, and performance profiling.",
        "Key concepts include JSX, props, state, lifecycle methods (or Hooks), and reconciliation.",
        "React is used for building single-page applications (SPAs), complex user interfaces, and mobile apps (React Native)."
    ],
    "MongoDB": [
        "MongoDB is a document database using BSON; common patterns include flexible schema design, indexing, and aggregations.",
        "Production setups consider replica sets for high availability, sharding for horizontal scaling, backups, and monitoring.",
        "It's a NoSQL database, offering high performance, high availability, and easy scalability.",
        "Common operations include CRUD (Create, Read, Update, Delete), aggregation pipelines, and indexing for query optimization."
    ],
    "HTML": [
        "HTML defines the structure of a web page using elements such as div, header, footer, and semantic tags (e.g., article, section, nav).",
        "Performance bottlenecks in HTML can come from too many DOM nodes, blocking resources (scripts/stylesheets), or inline styles/scripts. Optimization involves minimizing DOM, deferring non-critical resources, and optimizing asset loading.",
        "A production-ready HTML app emphasizes semantic markup for accessibility and SEO, responsive layout with viewports, and optimized asset delivery.",
        "It uses tags to structure content like headings, paragraphs, lists, links, and images."
    ],
    "CSS": [
        "CSS is used to style web pages, including layout, colors, fonts, and responsiveness.",
        "Responsive design is achieved using media queries, Flexbox, and Grid for adaptable layouts across devices.",
        "Common challenges include cross-browser compatibility, specificity conflicts (resolved by using BEM, CSS modules, or utility-first CSS), and maintaining modular and scalable styles.",
        "It controls the visual presentation of HTML elements, including colors, fonts, spacing, and positioning."
    ]
}

# Display overall interview stats at the top
if st.session_state.get("total_interview_time") is not None:
    total_time_seconds = st.session_state.total_interview_time
    minutes = total_time_seconds // 60
    seconds = total_time_seconds % 60
    st.markdown(f"### Interview Session Summary")
    st.info(f"Total Interview Time: {minutes}m {seconds}s")
else:
    st.info("No interview session data found. Complete an interview on '2_Questions' page.")


# Collect evaluations
rows = []
for sk, qa_list in generated_qa.items():
    for i, qa_item in enumerate(qa_list, start=1):
        q = qa_item['q']
        ans = qa_item['a'].strip() # Get the answer directly from our stored structure

        refs = REFERENCE_SNIPPETS.get(sk, [
            "A strong answer explains core concepts, trade-offs, and production concerns."
        ])

        score = 0.0
        best_match = ""
        if ans:
            eval_result = evaluate_answer(ans, refs)
            score = eval_result["score"]
            best_match = eval_result["best_match"]

        # Retrieve time spent for this specific question
        time_spent_q = st.session_state.question_timers.get((sk, i - 1), 0) # Q# is 1-indexed, so q_index is i-1

        rows.append({
            "Skill": sk,
            "Q#": i,
            "Question": q,
            "Answer": ans if ans else "(not answered)",
            "Score": score,
            "Time Spent (s)": time_spent_q, # Add time spent here
            "Closest Reference": best_match
        })

df = pd.DataFrame(rows)

st.markdown("### Detailed Question Evaluation")
# Show Q–A–Score table with Time Spent
if not df.empty:
    st.dataframe(df, width='stretch')
else:
    st.info("No questions have been answered yet.")

# Average score metric
# Calculate average only for questions that were actually answered
avg = df[df["Answer"] != "(not answered)"]["Score"].mean() if not df[df["Answer"] != "(not answered)"].empty else 0.0
st.metric("Average Score (of answered questions)", f"{avg:.1f}")


# Load taxonomy & suggest next skills
taxonomy = load_taxonomy("data/skills_taxonomy.json")
all_skills = build_skill_index(taxonomy)
resume_skills = st.session_state.get("resume_skills", [])

NEXT_SKILL_SUGGESTIONS = {
    "React": ["Next.js", "TypeScript", "Redux Toolkit", "GraphQL", "Jest", "Cypress"],
    "Node.js": ["NestJS", "TypeScript", "Docker", "Microservices", "Kafka", "Redis"],
    "Python": ["FastAPI", "PyTorch", "MLOps", "Django REST Framework", "Celery", "Pandas (Advanced)"],
    "MongoDB": ["Mongoose", "Sharding", "Redis", "Elasticsearch", "Data Modeling (NoSQL)"],
    "Docker": ["Kubernetes", "CI/CD", "Terraform", "Helm", "Prometheus", "Grafana"],
    "HTML": ["Accessibility (WCAG)", "SEO Best Practices", "Web Performance Optimization", "PWA (Progressive Web Apps)", "Semantic HTML5"],
    "CSS": ["Sass/Less", "Tailwind CSS", "CSS-in-JS (e.g., Styled Components)", "BEM Methodology", "CSS Grid Layout (Advanced)", "Animations"]
}


suggestions = []
for s in resume_skills:
    suggestions.extend(NEXT_SKILL_SUGGESTIONS.get(s, []))

# Keep only new skills found in taxonomy
suggestions = [s for s in suggestions if s in all_skills and s not in resume_skills]
suggestions = sorted(set(suggestions))

st.subheader("Suggested Next Skills")
if suggestions:
    st.write(", ".join(suggestions))
else:
    st.write("Based on your current skills, consider deepening knowledge in architecture, testing, and DevOps.")