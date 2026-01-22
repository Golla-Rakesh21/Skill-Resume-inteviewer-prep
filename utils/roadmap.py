import json
from typing import Dict, List, Any

def load_learning_resources(path: str) -> Dict[str, List[Dict[str, Any]]]:
    """Loads the learning resources mapping from a JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def generate_learning_roadmap(missing_skills: List[str], resources: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generates a personalized learning plan based on missing skills.

    Args:
        missing_skills: A list of skills the user needs to learn.
        resources: A dictionary where keys are skill names and values are lists of learning resources.

    Returns:
        A dictionary where keys are the missing skills and values are the corresponding learning resources.
    """
    roadmap = {}
    for skill in missing_skills:
        if skill in resources:
            roadmap[skill] = resources[skill]
    return roadmap