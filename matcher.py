def calculate_match_score(resume_skills, jd_skills):

    # Remove duplicates
    resume_skills = set(resume_skills)
    jd_skills = set(jd_skills)

    # Find matched and missing skills
    matched = sorted(list(resume_skills.intersection(jd_skills)))
    missing = sorted(list(jd_skills.difference(resume_skills)))

    # Prevent division by zero
    if not jd_skills:
        score = 0.0
    else:
        score = (len(matched) / len(jd_skills)) * 100

    return round(score, 2), matched, missing