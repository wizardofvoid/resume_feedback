import streamlit as st
import json
import os
import pandas as pd

# DB imports
from database.db import init_db, insert_resume, insert_jd, insert_match, fetch_recent_matches

# UI imports
from ui.theme import get_theme_tokens, setup_theme
from ui.components import render_score_gauge, render_skill_tags, section_divider, section_label, stat_block

# Import heavy modules only when needed
def get_imports():
    from parsers.resume_parser import parse_resume
    from parsers.jd_parser import extract_skills_from_JD
    from scoring.matcher import calculate_weighted_skill_match, calculate_format_score, calculate_ats_score
    from scoring.feedback import generate_feedback
    import google.generativeai as genai
    return parse_resume, extract_skills_from_JD, calculate_weighted_skill_match, calculate_format_score, calculate_ats_score, generate_feedback, genai

@st.cache_data
def load_skills_database():
    base_dir = os.path.dirname(__file__)
    try_paths = [
        os.path.join(base_dir, 'data', 'skills_list.json'),
        os.path.join(base_dir, 'data', 'skill_list.json'),
    ]
    for p in try_paths:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
    st.error("skills_list.json not found!")
    return []


@st.cache_data
def cached_parse_resume(file_input, skills_db):
    parse_resume, _, _, _, _, _, _ = get_imports()
    return parse_resume(file_input, skills_db)

@st.cache_data
def cached_extract_skills_from_JD(job_description, skills_db):
    _, extract_skills_from_JD, _, _, _, _, _ = get_imports()
    return extract_skills_from_JD(job_description, skills_db)

@st.cache_data
def resume_feedback(resume_text, job_description=""):
    _, _, _, _, _, generate_feedback, genai = get_imports()
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    except:
        return "API key missing"

    system_msg = "You are an expert technical recruiter..."
    user_prompt = ("Job Description:\n" + job_description + "\n\n" if job_description else "") + \
                  "Resume Text:\n" + resume_text

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        generation_config={"temperature": 0.3, "max_output_tokens": 800}
    )
    prompt = system_msg + "\n\n" + user_prompt
    response = model.generate_content(prompt)
    return (response.text or "").strip()


# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeATS Pro",
    page_icon="R",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── THEME ───────────────────────────────────────────────────────────────────
T, is_dark = get_theme_tokens()
setup_theme(T, is_dark)

col_title, col_toggle = st.columns([5, 1])
with col_toggle:
    toggle_label = "Light" if is_dark else "Dark"
    if st.button(toggle_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

skills_db = load_skills_database()
init_db()

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:0.25rem;">
    <span style="
        display:inline-block; padding:0.2rem 0.5rem;
        border:1px solid {{T['border']}}; border-radius:4px;
        color:{{T['text_tertiary']}}; font-size:0.65rem; font-weight:500;
        letter-spacing:0.04em; text-transform:uppercase;
        margin-bottom:0.75rem;
    ">ATS Resume Scorer</span>
</div>
""", unsafe_allow_html=True)

st.title("ResumeATS Pro")

st.markdown(f"""<p style="
    color:{{T['text_secondary']}}; font-size:0.9rem; margin:-0.25rem 0 1.5rem 0; line-height:1.5;
">Upload your resume and paste a job description to get an ATS compatibility score,
skill gap analysis, and AI feedback.</p>""", unsafe_allow_html=True)


# ─── INPUT ───────────────────────────────────────────────────────────────────
section_divider(T)
section_label("Input", T)

col_upload, col_jd = st.columns(2, gap="medium")

with col_upload:
    st.markdown(f'<div style="color:{{T["text_secondary"]}}; font-weight:500; font-size:0.8rem; margin-bottom:0.4rem;">Resume</div>',
                unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=['pdf', 'docx'], label_visibility="collapsed")

with col_jd:
    st.markdown(f'<div style="color:{{T["text_secondary"]}}; font-weight:500; font-size:0.8rem; margin-bottom:0.4rem;">Job Description</div>',
                unsafe_allow_html=True)
    job_description = st.text_area("Paste Job Description", height=180, label_visibility="collapsed",
                                   placeholder="Paste the full job description here...")

st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)
analyze_clicked = st.button("Analyze Resume", use_container_width=True)


# ─── RESULTS ─────────────────────────────────────────────────────────────────
if analyze_clicked:
    if not resume_file or not job_description.strip():
        st.error("Please upload a resume and paste the job description.")
    else:
        with st.spinner("Analyzing..."):
            parse_resume, _, calculate_weighted_skill_match, calculate_format_score, calculate_ats_score, generate_feedback, _ = get_imports()
            resume_data = cached_parse_resume(resume_file, skills_db)

            if resume_data.get('is_scanned', False):
                st.error("Scanned resume detected. Please upload a text-based PDF or DOCX.")
            else:
                job_skill_weights = cached_extract_skills_from_JD(job_description, skills_db)
                resume_skills_set = {skill.lower().strip() for skill in resume_data.get('skills', [])}

                skill_match_score = calculate_weighted_skill_match(resume_skills_set, job_skill_weights)
                format_score = calculate_format_score(resume_data)
                ats_score = calculate_ats_score(skill_match_score, format_score)

                # ── Score ──
                section_divider(T)
                section_label("ATS Score", T)

                col_gauge, col_stats = st.columns([1, 1], gap="medium")

                with col_gauge:
                    render_score_gauge(ats_score, T)

                with col_stats:
                    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
                    stat_block("Skill Match", f"{skill_match_score:.1f}%", T, T['accent'])
                    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                    stat_block("Format Score", f"{format_score:.1f}%", T, T['accent'])

                st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                st.progress(ats_score / 100)

                # ── Skills ──
                if job_skill_weights:
                    job_skills_normalized = set(job_skill_weights.keys())
                    found_skills = resume_skills_set & job_skills_normalized
                    missing_skills = job_skills_normalized - resume_skills_set

                    section_divider(T)
                    section_label(f"Skills  /  {len(found_skills)} matched, {len(missing_skills)} missing", T)

                    render_skill_tags(found_skills, missing_skills, job_skill_weights, T)

                    with st.expander("Detailed skill table"):
                        rows = []
                        for sk in found_skills:
                            rows.append({"Skill": sk.title(), "Status": "Found", "Weight": job_skill_weights[sk]})
                        for sk in missing_skills:
                            rows.append({"Skill": sk.title(), "Status": "Missing", "Weight": job_skill_weights[sk]})
                        df = pd.DataFrame(rows).sort_values(by=["Weight", "Skill"], ascending=[False, True])
                        st.dataframe(df, use_container_width=True, hide_index=True)

                # ── AI Feedback ──
                section_divider(T)
                section_label("AI Feedback", T)

                with st.spinner("Generating feedback..."):
                    llm_feedback = resume_feedback(resume_data.get('text', ''), job_description)

                st.markdown(f"""<div style="
                    padding:1rem 1.25rem; border:1px solid {{T['border']}}; border-radius:6px;
                    background:{{T['bg']}}; color:{{T['text_primary']}};
                    line-height:1.65; font-size:0.85rem;
                ">{llm_feedback}</div>""", unsafe_allow_html=True)

                # ── DB Store ──
                resume_id = insert_resume(
                    resume_data.get('text', ''),
                    resume_data.get('skills', []),
                    resume_data.get('contact_info', {}).get('email', ''),
                    resume_data.get('contact_info', {}).get('phone', '')
                )
                jd_id = insert_jd(job_description, job_skill_weights)
                insert_match(resume_id, jd_id, skill_match_score, format_score,
                             ats_score, list(missing_skills), llm_feedback)
                st.success("Analysis saved.")


# ─── HISTORY ─────────────────────────────────────────────────────────────────
section_divider(T)
section_label("History", T)

records = fetch_recent_matches(limit=10)

if records:
    df = pd.DataFrame(records, columns=[
        "Match ID", "Timestamp", "Final ATS Score",
        "Resume ID", "Email", "Phone", "JD ID"
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.markdown(f"""<div style="
        text-align:center; padding:2rem 0; color:{{T['text_tertiary']}}; font-size:0.85rem;
    ">No history yet. Analyze a resume to see results here.</div>""", unsafe_allow_html=True)


# ─── DEBUG ───────────────────────────────────────────────────────────────────
with st.expander("Debug data"):
    if resume_file:
        resume_data = cached_parse_resume(resume_file, skills_db)
        st.json(resume_data.get('contact_info', {}))
        st.json(resume_data.get('skills', []))
    else:
        st.info("Upload a resume to view extracted data.")


# ─── CLEAR ───────────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
col_l, col_c, col_r = st.columns([3, 1, 3])
with col_c:
    import sqlite3
    if st.button("Clear History", use_container_width=True):
        conn = sqlite3.connect("data/app.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM matches;")
        conn.commit()
        conn.close()
        st.success("History cleared. Refresh the page.")


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown(f"""<div style="
    text-align:center; padding:2rem 0 0.5rem 0;
    color:{{T['text_tertiary']}}; font-size:0.7rem;
    border-top:1px solid {{T['border']}}; margin-top:2rem;
">ResumeATS Pro</div>""", unsafe_allow_html=True)
