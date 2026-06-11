import streamlit as st
import requests
import pandas as pd

# UI imports
from ui.theme import get_theme_tokens, setup_theme
from ui.components import render_score_gauge, render_skill_tags, section_divider, section_label, stat_block

API_URL = "http://localhost:8000"

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
section_divider(T)
section_label("Input", T)

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
    if not resume_file:
        st.error("Please upload a resume.")
    else:
        with st.spinner("Analyzing on backend..."):
            try:
                files = {"file": (resume_file.name, resume_file.getvalue(), "application/octet-stream")}
                data = {"job_description": job_description}
                response = requests.post(f"{API_URL}/analyze", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    ats_score = result["ats_score"]
                    skill_match_score = result["skill_match_score"]
                    format_score = result["format_score"]
                    found_skills = set(result["found_skills"])
                    missing_skills = set(result["missing_skills"])
                    job_skill_weights = result["job_skill_weights"]
                    ai_feedback = result["ai_feedback"]
                    
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
                        section_divider(T)
                        section_label(f"Skills  /  {len(found_skills)} matched, {len(missing_skills)} missing", T)

                        render_skill_tags(found_skills, missing_skills, job_skill_weights, T)

                        with st.expander("Detailed skill table"):
                            data_table = []
                            for s, w in job_skill_weights.items():
                                status = "Found" if s in found_skills else "Missing"
                                data_table.append({"Skill": s, "Weight": w, "Status": status})
                            if data_table:
                                st.dataframe(pd.DataFrame(data_table), use_container_width=True, hide_index=True)
                    elif found_skills:
                        section_divider(T)
                        section_label(f"Skills Found ({len(found_skills)})", T)
                        
                        # Render a simple list of found skills
                        tags_html = "".join([
                            f'<span style="display:inline-block; padding:0.3rem 0.6rem; margin:0 0.4rem 0.4rem 0; '
                            f'background-color:{T["surface"]}; color:{T["text_primary"]}; '
                            f'border:1px solid {T["border"]}; border-radius:4px; font-size:0.8rem;">'
                            f'{skill}</span>'
                            for skill in found_skills
                        ])
                        st.markdown(f'<div style="margin-bottom:1rem;">{tags_html}</div>', unsafe_allow_html=True)

                    # ── AI Feedback ──
                    if ai_feedback:
                        section_divider(T)
                        section_label("AI Feedback", T)
                        st.info(ai_feedback)

                else:
                    st.error(f"Backend Error: {response.json().get('detail', response.text)}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend API. Please make sure the FastAPI server is running on localhost:8000.")


# ─── HISTORY ─────────────────────────────────────────────────────────────────
section_divider(T)
section_label("History", T)

col_l, col_c, col_r = st.columns([2, 1, 2])
with col_c:
    if st.button("Clear History", use_container_width=True):
        try:
            res = requests.post(f"{API_URL}/clear_history")
            if res.status_code == 200:
                st.success("History cleared.")
        except Exception:
            st.error("Failed to clear history.")

try:
    history_res = requests.get(f"{API_URL}/history")
    if history_res.status_code == 200:
        history_data = history_res.json()["history"]
        if history_data:
            df = pd.DataFrame(history_data)
            st.dataframe(
                df[['created_at', 'email', 'score']],
                use_container_width=True, hide_index=True
            )
        else:
            st.info("No history found.")
except requests.exceptions.ConnectionError:
    st.warning("Cannot connect to backend to load history.")

# ─── FOOTER ─────────────
st.markdown(f"""<div style="
    text-align:center; padding:2rem 0 0.5rem 0;
    color:{T['text_tertiary']}; font-size:0.7rem;
    border-top:1px solid {T['border']}; margin-top:2rem;
">ResumeATS Pro</div>""", unsafe_allow_html=True)