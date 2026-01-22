
import random
from typing import List, Dict

TEMPLATES = {
    "beginner": [
        "What is {skill}, and where is it commonly used?",
        "Explain core concepts of {skill} that a newcomer must know.",
        "List three practical use-cases for {skill}.",
        "What tools or libraries are often used with {skill}?",
    ],
    "intermediate": [
        "Describe a real project where you used {skill}. What challenges did you face and how did you solve them?",
        "Compare {skill} with an alternative. When would you choose one over the other?",
        "How would you structure a production-ready application using {skill}?",
        "Explain common performance bottlenecks when using {skill} and how to mitigate them.",
    ],
    "advanced": [
        "Design a scalable architecture that leverages {skill} under high load. Explain trade-offs.",
        "How would you debug and optimize a complex system built with {skill}?",
        "What are the major limitations of {skill} in production, and how do you work around them?",
        "Propose a migration strategy from a legacy stack to {skill} with minimal downtime.",
    ],
    "coding": [
        "Write a function using {skill} to solve: Given a list of integers, return the length of the longest increasing subsequence.",
        "Implement a service in {skill} that exposes a REST endpoint `/health` and returns uptime seconds.",
        "Given a large file, stream it line-by-line in {skill} and count unique users efficiently.",
        "Using {skill}, connect to a database and perform a parameterized query to fetch the last 50 records.",
    ]
}

SKILL_TO_CATEGORY = {
    "Python": "coding", "Java": "coding", "JavaScript": "coding", "TypeScript": "coding", "C++": "coding", "C#": "coding", "Go": "coding", "Kotlin": "coding", "Swift": "coding",
    "React": "intermediate", "Next.js": "intermediate", "Angular": "intermediate", "Vue": "intermediate",
    "Node.js": "coding", "Express": "intermediate", "Django": "intermediate", "Flask": "intermediate", "Spring Boot": "intermediate",
    "MongoDB": "intermediate", "MySQL": "intermediate", "PostgreSQL": "intermediate",
    "Docker": "intermediate", "Kubernetes": "advanced", "AWS": "advanced", "Azure": "advanced", "GCP": "advanced"
}

def generate_questions(skill: str, level: str, n: int = 5) -> List[str]:
    level = level.lower()
    bucket = level if level in TEMPLATES else "beginner"
    base = list(TEMPLATES[bucket])

    # add a coding angle if the skill is a coding language/tool
    category = SKILL_TO_CATEGORY.get(skill, None)
    if category == "coding":
        base += TEMPLATES["coding"]

    random.shuffle(base)
    return [q.format(skill=skill) for q in base[:n]]
