import re
from typing import List, Dict, Any
from collections import Counter
from .skills import compare_with_job_desc, fuzzy_find_skills

# A simple list of common English stop words. A library like NLTK would be more robust.
STOP_WORDS = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
    'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
    'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
    'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
    'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
])

ACTION_VERBS = [
    'architected', 'automated', 'built', 'coded', 'completed', 'created', 'debugged',
    'delivered', 'designed', 'developed', 'deployed', 'directed', 'engineered',
    'executed', 'formalized', 'implemented', 'improved', 'integrated', 'launched',
    'led', 'managed', 'mentored', 'optimized', 'owned', 'planned', 'prototyped',
    'refactored', 'released', 'resolved', 'restructured', 'revamped', 'scaled',
    'shipped', 'spearheaded', 'streamlined', 'supported', 'tested', 'upgraded'
]

def _extract_keywords(text: str) -> List[str]:
    """Extracts non-stop-word keywords from text."""
    text = re.sub(r'[^\w\s]', '', text.lower()) # Remove punctuation
    words = text.split()
    return [word for word in words if word not in STOP_WORDS and not word.isdigit()]

def calculate_ats_score(resume_text: str, job_desc_text: str, all_skills: List[str]) -> Dict[str, Any]:
    """
    Calculates a comprehensive ATS score based on multiple factors.
    Returns a dictionary with the total score and a breakdown of sub-scores.
    """
    results = {}

    # --- 1. Skill Match (Weight: 50%) ---
    resume_skills = fuzzy_find_skills(resume_text, all_skills)
    jd_skills = fuzzy_find_skills(job_desc_text, all_skills)
    
    if not jd_skills:
        skill_score = 0
    else:
        common_skills = set(resume_skills).intersection(jd_skills)
        skill_score = (len(common_skills) / len(jd_skills)) * 100
    results['skill_match'] = {'score': round(skill_score), 'details': f"{len(common_skills)} of {len(jd_skills)} required skills found."}

    # --- 2. Keyword Density (Weight: 20%) ---
    resume_keywords = Counter(_extract_keywords(resume_text))
    jd_keywords = Counter(_extract_keywords(job_desc_text))
    
    # Get top 20 most frequent keywords from JD (excluding skills already counted)
    jd_top_keywords = {kw for kw, count in jd_keywords.most_common(20) if kw not in all_skills}
    
    if not jd_top_keywords:
        keyword_score = 0
    else:
        found_keywords = sum(1 for kw in jd_top_keywords if resume_keywords[kw] > 0)
        keyword_score = (found_keywords / len(jd_top_keywords)) * 100
    results['keyword_density'] = {'score': round(keyword_score), 'details': f"{found_keywords} of {len(jd_top_keywords)} key terms found."}


    # --- 3. Action Verbs (Weight: 15%) ---
    resume_lower = resume_text.lower()
    verb_count = sum(1 for verb in ACTION_VERBS if verb in resume_lower)
    # Normalize score: 100% if 10 or more verbs are found
    verb_score = min((verb_count / 10) * 100, 100)
    results['action_verbs'] = {'score': round(verb_score), 'details': f"{verb_count} action verbs found."}

    # --- 4. Measurable Metrics (Weight: 15%) ---
    metric_patterns = r'(\d+[\.,]?\d*%)|(\$\d[\d,\.]*)|(increased by \d+)|(reduced by \d+)|(\d+x)|(\d+\s?(ms|sec|min))'
    metrics_found = len(re.findall(metric_patterns, resume_text, re.IGNORECASE))
    # Normalize score: 100% if 5 or more metrics are found
    metric_score = min((metrics_found / 5) * 100, 100)
    results['measurable_metrics'] = {'score': round(metric_score), 'details': f"{metrics_found} quantifiable results found."}
    
    # --- Final Weighted Score ---
    total_score = (
        skill_score * 0.50 +
        keyword_score * 0.20 +
        verb_score * 0.15 +
        metric_score * 0.15
    )

    results['total_score'] = round(total_score)
    return results