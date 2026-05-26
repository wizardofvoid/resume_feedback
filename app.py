import streamlit as st
import json
import os
import pandas as pd
import math

# DB imports
from db import init_db, insert_resume, insert_jd, insert_match, fetch_recent_matches


# Import heavy modules only when needed
def get_imports():
    from resume_parser import parse_resume
    from JD_parser import extract_skills_from_JD
    from matcher import calculate_weighted_skill_match, calculate_format_score, calculate_ats_score
    from feedback import generate_feedback
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

# ─── THEME STATE ─────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

is_dark = st.session_state.theme == "dark"

# ─── THEME TOKENS ────────────────────────────────────────────────────────────
if is_dark:
    T = {
        "bg":              "#111113",
        "bg_secondary":    "#18181b",
        "surface":         "#1e1e22",
        "surface_hover":   "#252529",
        "border":          "#2a2a2e",
        "border_subtle":   "#222226",
        "text_primary":    "#ededef",
        "text_secondary":  "#a1a1a6",
        "text_tertiary":   "#6e6e76",
        "accent":          "#7c7cff",
        "accent_dim":      "rgba(124, 124, 255, 0.1)",
        "accent_border":   "rgba(124, 124, 255, 0.2)",
        "green":           "#3dd68c",
        "green_dim":       "rgba(61, 214, 140, 0.1)",
        "green_border":    "rgba(61, 214, 140, 0.2)",
        "red":             "#f87171",
        "red_dim":         "rgba(248, 113, 113, 0.1)",
        "red_border":      "rgba(248, 113, 113, 0.2)",
        "amber":           "#fbbf24",
        "amber_dim":       "rgba(251, 191, 36, 0.1)",
        "amber_border":    "rgba(251, 191, 36, 0.2)",
        "input_bg":        "#141416",
        "scrollbar":       "#2a2a2e",
    }
else:
    T = {
        "bg":              "#ffffff",
        "bg_secondary":    "#fafafa",
        "surface":         "#f5f5f7",
        "surface_hover":   "#eeeeef",
        "border":          "#e4e4e7",
        "border_subtle":   "#ebebee",
        "text_primary":    "#18181b",
        "text_secondary":  "#71717a",
        "text_tertiary":   "#a1a1aa",
        "accent":          "#5b5bd6",
        "accent_dim":      "rgba(91, 91, 214, 0.06)",
        "accent_border":   "rgba(91, 91, 214, 0.15)",
        "green":           "#16a34a",
        "green_dim":       "rgba(22, 163, 74, 0.06)",
        "green_border":    "rgba(22, 163, 74, 0.15)",
        "red":             "#dc2626",
        "red_dim":         "rgba(220, 38, 38, 0.06)",
        "red_border":      "rgba(220, 38, 38, 0.15)",
        "amber":           "#d97706",
        "amber_dim":       "rgba(217, 119, 6, 0.06)",
        "amber_border":    "rgba(217, 119, 6, 0.15)",
        "input_bg":        "#ffffff",
        "scrollbar":       "#d4d4d8",
    }

# ─── CSS ─────────────────────────────────────────────────────────────────────
css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── Reset ── */
*, *::before, *::after {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {{
    background: {T['bg']} !important;
    color: {T['text_primary']} !important;
}}

[data-testid="stHeader"] {{
    background: {T['bg']} !important;
    border-bottom: 1px solid {T['border_subtle']} !important;
}}

[data-testid="stSidebar"] {{
    background: {T['bg_secondary']} !important;
    border-right: 1px solid {T['border']} !important;
}}

.block-container {{
    max-width: 780px !important;
    padding: 2rem 1.5rem 3rem 1.5rem !important;
}}

/* ── Typography ── */
h1 {{
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: {T['text_primary']} !important;
    letter-spacing: -0.03em !important;
    margin-bottom: 0 !important;
}}

h2 {{
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: {T['text_secondary']} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    margin-top: 0 !important;
    margin-bottom: 0.75rem !important;
}}

h3 {{
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: {T['text_primary']} !important;
}}

/* ── Cards / Borders ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {{
    background: {T['bg']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
    padding: 1.25rem !important;
    box-shadow: none !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: {T['text_primary']} !important;
    color: {T['bg']} !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    letter-spacing: -0.01em !important;
    box-shadow: none !important;
    transition: opacity 0.15s ease !important;
    cursor: pointer !important;
    white-space: nowrap !important;
    min-height: 2.5rem !important;
}}

.stButton > button:hover {{
    opacity: 0.85 !important;
    transform: none !important;
    box-shadow: none !important;
}}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {{
    background: {T['surface']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
    padding: 1.25rem !important;
    transition: border-color 0.15s ease !important;
    height: 180px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}}

[data-testid="stFileUploader"]:hover {{
    border-color: {T['text_tertiary']} !important;
}}

/* Upload button — icon only */
[data-testid="stFileUploader"] button,
[data-testid="stFileUploaderDropzone"] button {{
    background: {T['bg']} !important;
    border: 1px solid {T['border']} !important;
    color: {T['text_secondary']} !important;
    border-radius: 6px !important;
    padding: 0.4rem 0.8rem !important;
    font-size: 0 !important;
    box-shadow: none !important;
    min-width: 36px !important;
    min-height: 32px !important;
    transition: border-color 0.15s ease !important;
}}

[data-testid="stFileUploader"] button::after,
[data-testid="stFileUploaderDropzone"] button::after {{
    content: 'Browse files' !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: {T['text_secondary']} !important;
}}

[data-testid="stFileUploader"] button:hover,
[data-testid="stFileUploaderDropzone"] button:hover {{
    border-color: {T['text_tertiary']} !important;
}}

[data-testid="stFileUploaderDropzone"] button > div > span,
[data-testid="stFileUploaderDropzone"] button > div > p,
[data-testid="stFileUploaderDropzone"] button p {{
    display: none !important;
}}

[data-testid="stFileUploaderDropzone"] {{
    background: transparent !important;
    color: {T['text_tertiary']} !important;
}}

[data-testid="stFileUploaderDropzone"] small {{
    color: {T['text_tertiary']} !important;
}}

[data-testid="stFileUploader"] label {{
    color: {T['text_secondary']} !important;
}}

/* ── Textarea ── */
textarea {{
    background: {T['input_bg']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 6px !important;
    color: {T['text_primary']} !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.875rem !important;
    transition: border-color 0.15s ease !important;
    resize: none !important;
    height: 180px !important;
}}

textarea:focus {{
    border-color: {T['accent']} !important;
    box-shadow: 0 0 0 2px {T['accent_dim']} !important;
    outline: none !important;
}}

textarea::placeholder {{
    color: {T['text_tertiary']} !important;
}}

/* ── Labels ── */
.stTextArea label, .stFileUploader label, .stTextInput label {{
    color: {T['text_secondary']} !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.02em !important;
}}

/* ── Metrics ── */
[data-testid="stMetricValue"] {{
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: {T['text_primary']} !important;
    letter-spacing: -0.03em !important;
}}

[data-testid="stMetricLabel"] {{
    color: {T['text_tertiary']} !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-size: 0.7rem !important;
}}

/* ── Progress Bar ── */
[data-testid="stProgress"] > div > div > div {{
    background: {T['accent']} !important;
    border-radius: 2px !important;
    height: 4px !important;
}}

[data-testid="stProgress"] > div > div {{
    background: {T['surface']} !important;
    border-radius: 2px !important;
    height: 4px !important;
}}

/* ── DataFrame ── */
.stDataFrame {{
    border-radius: 6px !important;
    overflow: hidden !important;
    border: 1px solid {T['border']} !important;
}}

/* ── Alerts ── */
.stSuccess {{
    background: {T['green_dim']} !important;
    border-left: 3px solid {T['green']} !important;
    color: {T['green']} !important;
    border-radius: 4px !important;
}}

.stInfo {{
    background: {T['accent_dim']} !important;
    border-left: 3px solid {T['accent']} !important;
    color: {T['accent']} !important;
    border-radius: 4px !important;
}}

.stError {{
    background: {T['red_dim']} !important;
    border-left: 3px solid {T['red']} !important;
    color: {T['red']} !important;
    border-radius: 4px !important;
}}

/* ── Expander ── */
[data-testid="stExpander"] {{
    background: {T['bg']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 6px !important;
    overflow: hidden !important;
}}

.streamlit-expanderHeader,
[data-testid="stExpanderToggleDetails"] summary {{
    color: {T['text_secondary']} !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    background: transparent !important;
}}

.streamlit-expanderHeader:hover,
[data-testid="stExpanderToggleDetails"] summary:hover {{
    color: {T['text_primary']} !important;
}}

[data-testid="stExpander"] svg[data-testid="stExpanderToggleIcon"],
[data-testid="stExpander"] [data-testid="stIconMaterial"] {{
    font-size: 0 !important;
}}

[data-testid="stExpander"] summary > span:first-child {{
    font-size: 0px !important;
    width: 1rem !important;
    height: 1rem !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    overflow: hidden !important;
}}

[data-testid="stExpander"] summary > span:first-child::after {{
    content: '+' !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: {T['text_tertiary']} !important;
}}

[data-testid="stExpander"][open] summary > span:first-child::after {{
    content: '\\2212' !important;
}}

/* ── Divider ── */
hr {{
    border: none !important;
    height: 1px !important;
    background: {T['border']} !important;
    margin: 1.5rem 0 !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {T['scrollbar']}; border-radius: 2px; }}

/* ── Hide Defaults ── */
footer, #MainMenu {{ visibility: hidden !important; }}
</style>
"""

st.markdown(css, unsafe_allow_html=True)


# ─── THEME TOGGLE ────────────────────────────────────────────────────────────
col_title, col_toggle = st.columns([5, 1])
with col_toggle:
    toggle_label = "Light" if is_dark else "Dark"
    if st.button(toggle_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def render_score_gauge(score):
    """Minimal circular score gauge."""
    if score >= 70:
        color = T['green']
        label = "Strong match"
    elif score >= 40:
        color = T['amber']
        label = "Moderate match"
    else:
        color = T['red']
        label = "Weak match"

    r = 70
    c = 2 * math.pi * r
    offset = c - (score / 100) * c

    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; padding:1.5rem 0;">
        <svg width="180" height="180" viewBox="0 0 180 180">
            <circle cx="90" cy="90" r="{r}" fill="none"
                stroke="{T['surface']}" stroke-width="8"/>
            <circle cx="90" cy="90" r="{r}" fill="none"
                stroke="{color}" stroke-width="8"
                stroke-linecap="round"
                stroke-dasharray="{c}" stroke-dashoffset="{offset}"
                transform="rotate(-90 90 90)"
                style="transition: stroke-dashoffset 1s ease;"/>
            <text x="90" y="84" text-anchor="middle"
                fill="{T['text_primary']}" font-size="36" font-weight="700"
                font-family="Inter, sans-serif">{score:.0f}</text>
            <text x="90" y="104" text-anchor="middle"
                fill="{T['text_tertiary']}" font-size="11" font-weight="500"
                font-family="Inter, sans-serif">/ 100</text>
        </svg>
        <span style="
            margin-top:0.75rem; padding:0.25rem 0.75rem;
            border:1px solid {color}20; border-radius:4px;
            color:{color}; font-size:0.75rem; font-weight:500;
            background:{color}10;
        ">{label}</span>
    </div>
    """, unsafe_allow_html=True)


def render_skill_tags(found_skills, missing_skills, job_skill_weights):
    """Compact skill tags."""
    html = '<div style="display:flex; flex-wrap:wrap; gap:6px; margin:0.5rem 0 1rem 0;">'
    for sk in sorted(found_skills):
        w = job_skill_weights.get(sk, 0)
        html += f"""<span style="
            display:inline-flex; align-items:center; gap:4px;
            padding:0.3rem 0.65rem; border-radius:4px;
            background:{T['green_dim']}; border:1px solid {T['green_border']};
            color:{T['green']}; font-size:0.75rem; font-weight:500;
        ">{sk.title()} <span style="opacity:0.6; font-size:0.65rem;">{w}</span></span>"""
    for sk in sorted(missing_skills):
        w = job_skill_weights.get(sk, 0)
        html += f"""<span style="
            display:inline-flex; align-items:center; gap:4px;
            padding:0.3rem 0.65rem; border-radius:4px;
            background:{T['red_dim']}; border:1px solid {T['red_border']};
            color:{T['red']}; font-size:0.75rem; font-weight:500;
        ">{sk.title()} <span style="opacity:0.6; font-size:0.65rem;">{w}</span></span>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def section_divider():
    st.markdown(f'<div style="height:1px; background:{T["border"]}; margin:2rem 0 1.5rem 0;"></div>',
                unsafe_allow_html=True)


def section_label(text):
    st.markdown(f"""<h2 style="
        font-size:0.7rem; font-weight:600; color:{T['text_tertiary']};
        text-transform:uppercase; letter-spacing:0.08em;
        margin:0 0 0.75rem 0; padding:0;
    ">{text}</h2>""", unsafe_allow_html=True)


def stat_block(label, value, color=None):
    c = color or T['text_primary']
    st.markdown(f"""
    <div style="
        padding:1rem; border:1px solid {T['border']}; border-radius:6px;
        background:{T['bg']};
    ">
        <div style="font-size:0.65rem; font-weight:600; color:{T['text_tertiary']};
            text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.35rem;">{label}</div>
        <div style="font-size:1.5rem; font-weight:700; color:{c};
            letter-spacing:-0.03em; font-family:Inter,sans-serif;">{value}</div>
    </div>""", unsafe_allow_html=True)


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
        border:1px solid {T['border']}; border-radius:4px;
        color:{T['text_tertiary']}; font-size:0.65rem; font-weight:500;
        letter-spacing:0.04em; text-transform:uppercase;
        margin-bottom:0.75rem;
    ">ATS Resume Scorer</span>
</div>
""", unsafe_allow_html=True)

st.title("ResumeATS Pro")

st.markdown(f"""<p style="
    color:{T['text_secondary']}; font-size:0.9rem; margin:-0.25rem 0 1.5rem 0; line-height:1.5;
">Upload your resume and paste a job description to get an ATS compatibility score,
skill gap analysis, and AI feedback.</p>""", unsafe_allow_html=True)


# ─── INPUT ───────────────────────────────────────────────────────────────────
section_divider()
section_label("Input")

col_upload, col_jd = st.columns(2, gap="medium")

with col_upload:
    st.markdown(f'<div style="color:{T["text_secondary"]}; font-weight:500; font-size:0.8rem; margin-bottom:0.4rem;">Resume</div>',
                unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=['pdf', 'docx'], label_visibility="collapsed")

with col_jd:
    st.markdown(f'<div style="color:{T["text_secondary"]}; font-weight:500; font-size:0.8rem; margin-bottom:0.4rem;">Job Description</div>',
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
                section_divider()
                section_label("ATS Score")

                col_gauge, col_stats = st.columns([1, 1], gap="medium")

                with col_gauge:
                    render_score_gauge(ats_score)

                with col_stats:
                    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
                    stat_block("Skill Match", f"{skill_match_score:.1f}%", T['accent'])
                    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                    stat_block("Format Score", f"{format_score:.1f}%", T['accent'])

                st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
                st.progress(ats_score / 100)

                # ── Skills ──
                if job_skill_weights:
                    job_skills_normalized = set(job_skill_weights.keys())
                    found_skills = resume_skills_set & job_skills_normalized
                    missing_skills = job_skills_normalized - resume_skills_set

                    section_divider()
                    section_label(f"Skills  /  {len(found_skills)} matched, {len(missing_skills)} missing")

                    render_skill_tags(found_skills, missing_skills, job_skill_weights)

                    with st.expander("Detailed skill table"):
                        rows = []
                        for sk in found_skills:
                            rows.append({"Skill": sk.title(), "Status": "Found", "Weight": job_skill_weights[sk]})
                        for sk in missing_skills:
                            rows.append({"Skill": sk.title(), "Status": "Missing", "Weight": job_skill_weights[sk]})
                        df = pd.DataFrame(rows).sort_values(by=["Weight", "Skill"], ascending=[False, True])
                        st.dataframe(df, use_container_width=True, hide_index=True)

                # ── AI Feedback ──
                section_divider()
                section_label("AI Feedback")

                with st.spinner("Generating feedback..."):
                    llm_feedback = resume_feedback(resume_data.get('text', ''), job_description)

                st.markdown(f"""<div style="
                    padding:1rem 1.25rem; border:1px solid {T['border']}; border-radius:6px;
                    background:{T['bg']}; color:{T['text_primary']};
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
section_divider()
section_label("History")

records = fetch_recent_matches(limit=10)

if records:
    df = pd.DataFrame(records, columns=[
        "Match ID", "Timestamp", "Final ATS Score",
        "Resume ID", "Email", "Phone", "JD ID"
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.markdown(f"""<div style="
        text-align:center; padding:2rem 0; color:{T['text_tertiary']}; font-size:0.85rem;
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
    color:{T['text_tertiary']}; font-size:0.7rem;
    border-top:1px solid {T['border']}; margin-top:2rem;
">ResumeATS Pro</div>""", unsafe_allow_html=True)
