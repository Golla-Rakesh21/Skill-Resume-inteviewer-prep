
# Streamlit Resume Interviewer (Skills → Proficiency → Adaptive Questions)

A Streamlit app that:
1) Parses a resume (PDF/DOCX)
2) Extracts skills (with fuzzy matching against a small taxonomy)
3) Predicts proficiency per skill (heuristics + lightweight ML)
4) Generates adaptive interview questions (beginner/intermediate/advanced)
5) (Optional) Compares resume to a Job Description to find skill gaps
6) Lets the candidate answer and receive automatic feedback

> Works fully offline by default (template-based QGen + cosine-sim evaluation).
> You can optionally plug in OpenAI or a local HF model later.

## Quickstart

```bash
# 1) Create a venv (recommended)
python -m venv .venv && source .venv/bin/activate  # (Windows) .venv\Scripts\activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Run
streamlit run app.py
```

## Optional: Use Sentence-Transformers model offline
The app uses `sentence-transformers` (MiniLM) to compute embeddings for similarity scoring. 
The first run will download the model; later runs are offline.

## Project Structure
```
streamlit_resume_interviewer/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── data/
│   └── skills_taxonomy.json
├── utils/
│   ├── __init__.py
│   ├── parser.py
│   ├── skills.py
│   ├── proficiency.py
│   ├── questions.py
│   └── evaluator.py
└── pages/
    ├── 1_Skills_and_Proficiency.py
    ├── 2_Questions.py
    └── 3_Evaluation_and_Recommendations.py
```

## Environment Variables (Optional)
Copy `.env.example` → `.env` and fill in values if you want to use external LLMs later.
