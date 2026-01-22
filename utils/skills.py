
import json
import re
from typing import Dict, List, Tuple
from rapidfuzz import fuzz, process

def load_taxonomy(path: str) -> Dict[str, List[str]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def build_skill_index(taxonomy: Dict[str, List[str]]) -> List[str]:
    skill_list = []
    for _, skills in taxonomy.items():
        skill_list.extend(skills)
    return sorted(set(skill_list))

def fuzzy_find_skills(text: str, all_skills: List[str], threshold: int = 85) -> List[str]:
    """Find skills by fuzzy matching over the full resume text."""
    text_norm = text.lower()
    found = set()
    for sk in all_skills:
        # quick contains check (case-insensitive) OR fuzz ratio
        if sk.lower() in text_norm:
            found.add(sk)
        else:
            score = fuzz.partial_ratio(sk.lower(), text_norm[:20000])  # limit for speed
            if score >= threshold:
                found.add(sk)
    return sorted(found)

def skill_frequency(text: str, skill: str) -> int:
    pattern = re.compile(rf"\b{re.escape(skill)}\b", re.IGNORECASE)
    return len(pattern.findall(text or ""))

def compare_with_job_desc(resume_skills: List[str], jd_text: str, all_skills: List[str]) -> Tuple[List[str], List[str]]:
    """Return (present_in_resume_and_jd, missing_in_resume_but_in_jd)"""
    jd_found = fuzzy_find_skills(jd_text, all_skills, threshold=85)
    common = sorted(set(resume_skills).intersection(jd_found))
    missing = sorted(set(jd_found) - set(resume_skills))
    return common, missing
