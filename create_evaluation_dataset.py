# --- START OF FILE create_evaluation_dataset.py ---

import json
import pandas as pd
from pathlib import Path

# --- Configuration ---
SKILLS_TO_EVALUATE = ["Python", "React", "AWS", "SQL", "Docker"]
SNIPPETS_PER_SKILL = 100
OUTPUT_FILE = "evaluation_dataset.csv"

def create_dataset():
    """
    Reads resume snippets from data/resume_snippets.json and creates a
    CSV file that is ready for manual labeling.
    """
    print("--- Starting Dataset Creation ---")
    snippets_path = Path("data/resume_snippets.json")
    if not snippets_path.exists():
        print(f"FATAL ERROR: The file '{snippets_path}' was not found.")
        return

    try:
        with open(snippets_path, "r", encoding="utf-8") as f:
            all_snippets = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FATAL ERROR: Could not parse {snippets_path}. Error: {e}")
        return

    evaluation_data = []
    for skill in SKILLS_TO_EVALUATE:
        if skill in all_snippets:
            skill_snippets = all_snippets[skill][:SNIPPETS_PER_SKILL]
            for snippet in skill_snippets:
                evaluation_data.append({
                    "skill": skill,
                    "snippet": snippet,
                    "true_level": ""  # to be labeled manually
                })
        else:
            print(f"WARNING: Skill '{skill}' not found in JSON.")

    if not evaluation_data:
        print("No evaluation data collected. Please check SKILLS_TO_EVALUATE.")
        return

    df = pd.DataFrame(evaluation_data)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"\nSUCCESS! Created '{OUTPUT_FILE}' with {len(df)} rows.")
    print("Now open it in Excel/Sheets and fill 'true_level' with:")
    print("  - Beginner\n  - Intermediate\n  - Advanced")

if __name__ == "__main__":
    create_dataset()

# --- END OF FILE create_evaluation_dataset.py ---
