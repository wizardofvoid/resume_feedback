import re

def extract_skills_from_JD(job_description: str, skills_db: list) -> dict:
    """
    Extracts skills from a job description and returns a dictionary
    of their weights (1 for standard, 2 for mandatory/required).

    Args:
        job_description (str): The raw text of the job description.
        skills_db (list): The list of skills from skills_list.json.

    Returns:
        dict: A dictionary where keys are normalized skills and
              values are their weights.
    """
    job_description_lower = job_description.lower()
    skill_weights = {}

    # Create a set of normalized skills for fast lookup
    skills_db_normalized = {skill.lower().strip() for skill in skills_db}

    # Split into sentences or roughly chunks by punctuation to check context
    sentences = re.split(r'[.!?\n]', job_description_lower)
    
    # Keywords that suggest a skill is mandatory
    mandatory_keywords = ['required', 'must have', 'essential', 'minimum', 'prerequisite', 'mandatory', 'needs to have', 'must-have']

    for sentence in sentences:
        is_mandatory_sentence = any(kw in sentence for kw in mandatory_keywords)
        
        for skill in skills_db_normalized:
            try:
                # Need special handling for skills that start/end with non-word chars like .NET or C++
                # \b doesn't work well for them.
                escaped = re.escape(skill)
                # If it starts with an alphanumeric, use \b, else just match
                prefix = r'\b' if skill[0].isalnum() else r'(^|\s)'
                suffix = r'\b' if skill[-1].isalnum() else r'($|\s)'
                
                pattern = prefix + escaped + suffix
                
                if re.search(pattern, sentence):
                    current_weight = skill_weights.get(skill, 0)
                    new_weight = 2 if is_mandatory_sentence else 1
                    
                    if new_weight > current_weight:
                        skill_weights[skill] = new_weight
            except re.error:
                continue

    return skill_weights