import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

@st.cache_data(show_spinner="Optimizing your bullet point...")
def optimize_bullet_point(bullet_point: str, job_description: str) -> str:
    """
    Uses the Gemini API to rewrite a resume bullet point for greater impact.

    Args:
        bullet_point (str): The original bullet point from the user's resume.
        job_description (str): The target job description for context.

    Returns:
        str: A markdown-formatted string with optimized suggestions.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: Google API Key not found. Please configure it in your `.env` file."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # Provide context if a job description is available
    jd_context = "There is no specific job description for context."
    if job_description and job_description.strip():
        jd_context = f"The candidate is applying for a job with the following description: '{job_description[:1000]}...'" # Truncate for brevity

    prompt = f"""
    You are an expert career coach and professional resume writer. Your task is to rewrite a resume bullet point to make it more impactful.

    **Instructions:**
    1.  Analyze the original bullet point provided by the user.
    2.  Rewrite it in 3 different, improved ways.
    3.  Each suggestion should start with a strong action verb (e.g., "Engineered," "Architected," "Spearheaded," "Optimized").
    4.  Incorporate quantifiable metrics and results wherever possible. If the original text lacks numbers, suggest realistic placeholders like "[achieved X% growth]" or "[reduced latency by Y ms]".
    5.  Tailor the language and keywords to align with the provided job description context.
    6.  Keep each suggestion to a single, concise sentence.
    7.  Return the response in markdown format, with each suggestion as a bullet point.

    **Job Description Context:**
    {jd_context}

    **Original Bullet Point to Improve:**
    "{bullet_point}"

    **Your Rewritten Suggestions (in markdown):**
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating suggestions: {e}"