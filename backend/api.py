from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import shutil
import tempfile
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

from backend.parsers.resume_parser import parse_resume
from backend.parsers.jd_parser import extract_skills_from_JD
from backend.scoring.matcher import calculate_weighted_skill_match, calculate_format_score, calculate_ats_score
from backend.database.db import insert_resume, insert_jd, insert_match, fetch_recent_matches, init_db, clear_db
from backend.scoring.synonyms import get_canonical_name
import google.generativeai as genai

# Initialize database
init_db()

if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="Resume ATS API")

def get_skills_db():
    base_dir = Path(__file__).parent.parent
    skills_path = base_dir / 'backend' / 'data' / 'skills_list.json'
    if skills_path.exists():
        with open(skills_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...), job_description: str = Form("")):
    skills_db = get_skills_db()
    
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        resume_data = parse_resume(tmp_path, skills_db)
        if resume_data.get('is_scanned', False):
            raise HTTPException(status_code=400, detail="Scanned resume detected. Please upload a text-based PDF or DOCX.")

        resume_skills_set = {skill.lower().strip() for skill in resume_data.get('skills', [])}
        format_score = calculate_format_score(resume_data)

        if job_description.strip():
            job_skill_weights = extract_skills_from_JD(job_description, skills_db)
            skill_match_score = calculate_weighted_skill_match(resume_skills_set, job_skill_weights)
            ats_score = calculate_ats_score(skill_match_score, format_score)
            
            # Generate Feedback against JD
            system_msg = "You are an expert technical recruiter analyzing a candidate's resume against a job description. Provide constructive, brief feedback."
            user_prompt = "Job Description:\n" + job_description + "\n\nResume Text:\n" + resume_data.get('text', '')
            
            # Match using canonical names (synonyms/aliases)
            canonical_resume_skills = {get_canonical_name(s) for s in resume_skills_set}
            found_skills = []
            missing_skills = []
            for skill in job_skill_weights.keys():
                canonical_skill = get_canonical_name(skill)
                if canonical_skill in canonical_resume_skills:
                    found_skills.append(skill)
                else:
                    missing_skills.append(skill)
        else:
            job_skill_weights = {}
            skill_match_score = resume_data.get('quality_analysis', {}).get('ats_score', format_score) 
            ats_score = skill_match_score # Use holistic quality score as fallback ATS score
            
            # Generate General Feedback
            system_msg = "You are an expert technical recruiter reviewing a candidate's resume. Provide constructive, brief feedback on how to improve its impact and structure."
            user_prompt = "Resume Text:\n" + resume_data.get('text', '')
            
            found_skills = list(resume_skills_set)
            missing_skills = []

        ai_feedback = "AI Feedback disabled or missing API key."
        if api_key:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_msg)
                response = model.generate_content(user_prompt)
                ai_feedback = response.text
            except Exception as e:
                ai_feedback = f"Error generating feedback: {str(e)}"

        # Save to DB
        contact_info = resume_data.get('contact_info', {})
        rid = insert_resume(resume_data.get('text', ''), found_skills, contact_info.get('email', ''), contact_info.get('phone', ''))
        jdid = insert_jd(job_description, job_skill_weights)
        insert_match(rid, jdid, skill_match_score, format_score, ats_score, missing_skills, ai_feedback)

        return {
            "ats_score": ats_score,
            "skill_match_score": skill_match_score,
            "format_score": format_score,
            "found_skills": found_skills,
            "missing_skills": missing_skills,
            "job_skill_weights": job_skill_weights,
            "ai_feedback": ai_feedback,
            "quality_analysis": resume_data.get('quality_analysis', {})
        }

    finally:
        os.unlink(tmp_path)

@app.get("/history")
async def get_history():
    history = fetch_recent_matches()
    # match_id, created_at, final_ats_score, resume_id, contact_email, contact_phone, jd_id
    formatted = []
    for row in history:
        formatted.append({
            "id": row[0],
            "created_at": row[1],
            "score": row[2],
            "resume_id": row[3],
            "email": row[4],
            "phone": row[5],
            "jd_id": row[6]
        })
    return {"history": formatted}

@app.post("/clear_history")
async def clear_history():
    try:
        clear_db()
        return {"status": "cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear database: {str(e)}")
