import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

@st.cache_data(show_spinner="Analyzing job description and generating questions...")
def generate_behavioral_questions(job_description: str) -> str:
    """
    Uses the Gemini API to analyze a job description and generate relevant behavioral questions
    with STAR method guidance.

    Args:
        job_description (str): The target job description.

    Returns:
        str: A markdown-formatted string with questions and answering guidance.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: Google API Key not found. Please configure it in your `.env` file."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    You are an expert HR manager and career coach specializing in interview preparation.
    Your task is to analyze the provided job description and generate a set of tailored behavioral interview questions to help a candidate prepare.

    **Instructions:**
    1.  **Analyze the Job Description:** Carefully read the text below to identify key themes, cultural values, and required soft skills. Look for keywords like "collaboration," "fast-paced environment," "leadership," "ownership," "problem-solving," "adaptability," "communication," and "customer-focused."

    2.  **Generate 5 Questions:** Based on your analysis, create 5 distinct behavioral interview questions that an interviewer would likely ask for this role.

    3.  **Provide STAR Method Guidance:** For EACH of the 5 questions, you must provide guidance on how to structure an answer using the STAR method. Explain what the candidate should describe for each part:
        *   **S (Situation):** Briefly describe the context and background.
        *   **T (Task):** Explain what you were required to do, your goal, or the challenge you faced.
        *   **A (Action):** Detail the specific, concrete steps YOU took to address the situation. Focus on your individual contribution.
        *   **R (Result):** Quantify the outcome. What was the positive result of your actions? Use numbers, percentages, or concrete examples of success.

    4.  **Format the Output:** Structure your entire response in clear Markdown. Use a main heading for each question and then sub-bullets for the STAR guidance.

    **Job Description to Analyze:**
    ---
    {job_description}
    ---

    **Example Output Format:**
    ### Question 1: Tell me about a time you had to collaborate with a difficult team member.
    *   **S (Situation):** Describe a specific project or situation where you worked with a colleague whose work style or personality clashed with yours.
    *   **T (Task):** What was the team's overall goal, and what was your specific responsibility in that project?
    *   **A (Action):** What specific actions did you take to manage the relationship and ensure the project stayed on track? (e.g., "I scheduled a one-on-one meeting to understand their perspective...", "I suggested we define clear roles...").
    *   **R (Result):** What was the outcome? Did you successfully complete the project? Did your relationship with the colleague improve? (e.g., "As a result, we delivered the project on time and our communication improved significantly for future tasks.").

    Now, please generate the questions and guidance based on the job description provided.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating questions: {e}"