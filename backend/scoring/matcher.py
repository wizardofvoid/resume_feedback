from backend.scoring.synonyms import get_canonical_name

def calculate_weighted_skill_match(resume_skills_set: set, job_skill_weights: dict) -> float:
    """
    Calculates a skill match score. 
    job_skill_weights contains values of 1 (standard) or 2 (mandatory).

    Args:
        resume_skills_set (set): A set of normalized skills from the resume.
        job_skill_weights (dict): A dict where keys are normalized skills from the JD
                                  and values are their weight (1 or 2).

    Returns:
        float: A score from 0 to 100.
    """
    if not job_skill_weights:
        return 0.0

    # Convert resume skills to canonical names
    canonical_resume_skills = {get_canonical_name(s) for s in resume_skills_set}

    # Convert job description skill weights to canonical names, keeping the maximum weight if duplicates collapse
    canonical_job_weights = {}
    for skill, weight in job_skill_weights.items():
        canonical_skill = get_canonical_name(skill)
        canonical_job_weights[canonical_skill] = max(canonical_job_weights.get(canonical_skill, 0), weight)

    matched_score = 0
    total_possible_score = sum(canonical_job_weights.values())

    for skill in canonical_resume_skills:
        if skill in canonical_job_weights:
            matched_score += canonical_job_weights[skill]

    match_percentage = (matched_score / total_possible_score) * 100
    return min(match_percentage, 100.0)

def calculate_format_score(resume_data: dict) -> float:
    """
    Calculates a score based on the presence of key ATS-friendly sections,
    with intelligent fallbacks so candidates aren't penalized for creative section naming.

    Args:
        resume_data (dict): The full dictionary returned by the resume_parser.

    Returns:
        float: A score from 0 to 100.
    """
    score = 0
    
    # 1. Contact info (40 points max)
    contact_info = resume_data.get('contact_info', {})
    if contact_info.get('email'):
        score += 20
    if contact_info.get('phone'):
        score += 20

    # 2. Text volume / completeness fallback (20 points max)
    # If the resume has a decent amount of text, it's generally well-formatted enough to be parsed
    text = resume_data.get('text', '')
    word_count = len(text.split())
    if word_count > 150:
        score += 20
    elif word_count > 50:
        score += 10

    # 3. Key Sections or implicit presence (40 points max)
    # 20 for education, 20 for experience
    sections_detected = resume_data.get('sections_detected', {})
    has_education = bool(sections_detected.get('education', [])) or bool(resume_data.get('education'))
    has_experience = bool(sections_detected.get('experience', [])) or bool(resume_data.get('experience'))
    
    # Fallback logic:
    total_skills = resume_data.get('total_skills', len(resume_data.get('skills', [])))
    text_lower = text.lower()
    
    if has_education:
        score += 20
    elif "university" in text_lower or "college" in text_lower or "degree" in text_lower or "bachelor" in text_lower:
        score += 20

    if has_experience:
        score += 20
    elif total_skills > 5 and word_count > 200:
        # Implicitly grant experience points if they have enough technical substance and length
        score += 20
        
    return min(float(score), 100.0)

def calculate_ats_score(skill_match_score: float, format_score: float) -> float:
    """
    Calculates the final ATS score by combining skill match and format scores.
    Weighs skill match as 70% and format/completeness as 30%.

    Args:
        skill_match_score (float): The 0-100 score from calculate_weighted_skill_match.
        format_score (float): The 0-100 score from calculate_format_score.

    Returns:
        float: The final ATS score, rounded to two decimal places.
    """
    
    # Skill match is 70% of the score
    skill_component = skill_match_score * 0.70
    
    # Format friendliness is 30% of the score
    format_component = format_score * 0.30
    
    final_score = skill_component + format_component
    
    return round(final_score, 2)