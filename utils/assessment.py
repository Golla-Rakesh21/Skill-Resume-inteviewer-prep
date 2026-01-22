import os
import json
import re
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

@st.cache_data(show_spinner="Generating assessment...")
def generate_assessment(skills: list, difficulty: str, num_questions: int) -> list:
    """
    Generates a technical assessment using the Google Gemini API.

    Args:
        skills (list): A list of skills to base the assessment on.
        difficulty (str): The desired difficulty level (e.g., "Beginner", "Intermediate").
        num_questions (int): The number of questions to generate.

    Returns:
        list: A list of dictionaries, where each dictionary is a question object.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Google API Key not found. Please set it in your .env file.")
        return []

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    skill_str = ", ".join(skills)

    prompt = f"""
    You are an expert technical interviewer. Your task is to generate a multiple-choice quiz to assess a candidate's proficiency.

    Please generate a technical assessment with exactly {num_questions} multiple-choice questions based on the following criteria:
    1.  **Skills to assess:** {skill_str}
    2.  **Difficulty Level:** {difficulty}

    **IMPORTANT:** Your response MUST be a valid JSON array (a list of JSON objects) and nothing else. Do not include any text before or after the JSON array. Do not use markdown formatting like ```json.

    Each JSON object in the array must have the following four keys:
    -   `question`: A string containing the question text.
    -   `options`: A list of 4 strings representing the possible answers.
    -   `correct_answer`: A string that exactly matches one of the items in the `options` list.
    -   `explanation`: A brief string explaining why the correct answer is right.

    Example format:
    [
        {{
            "question": "What is the primary function of the `useEffect` hook in React?",
            "options": [
                "To manage component state",
                "To perform side effects in function components",
                "To handle routing",
                "To define component structure"
            ],
            "correct_answer": "To perform side effects in function components",
            "explanation": "useEffect is used for data fetching, subscriptions, or manually changing the DOM, which are all side effects."
        }}
    ]
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text

        # Clean the response text to ensure it's valid JSON
        # The model sometimes wraps the JSON in markdown backticks
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if not json_match:
            st.error("Failed to parse the assessment from the AI's response. The format was unexpected.")
            print("Unexpected AI Response:", response_text) # For debugging
            return []

        json_str = json_match.group(0)
        questions = json.loads(json_str)
        return questions

    except Exception as e:
        st.error(f"An error occurred while generating the assessment: {e}")
        return []