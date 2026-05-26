import streamlit as st
import math

def render_score_gauge(score, T):
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
            <circle cx="90" cy="90" r="{{r}}" fill="none"
                stroke="{{T['surface']}}" stroke-width="8"/>
            <circle cx="90" cy="90" r="{{r}}" fill="none"
                stroke="{{color}}" stroke-width="8"
                stroke-linecap="round"
                stroke-dasharray="{{c}}" stroke-dashoffset="{{offset}}"
                transform="rotate(-90 90 90)"
                style="transition: stroke-dashoffset 1s ease;"/>
            <text x="90" y="84" text-anchor="middle"
                fill="{{T['text_primary']}}" font-size="36" font-weight="700"
                font-family="Inter, sans-serif">{{score:.0f}}</text>
            <text x="90" y="104" text-anchor="middle"
                fill="{{T['text_tertiary']}}" font-size="11" font-weight="500"
                font-family="Inter, sans-serif">/ 100</text>
        </svg>
        <span style="
            margin-top:0.75rem; padding:0.25rem 0.75rem;
            border:1px solid {{color}}20; border-radius:4px;
            color:{{color}}; font-size:0.75rem; font-weight:500;
            background:{{color}}10;
        ">{{label}}</span>
    </div>
    """, unsafe_allow_html=True)


def render_skill_tags(found_skills, missing_skills, job_skill_weights, T):
    """Compact skill tags."""
    html = '<div style="display:flex; flex-wrap:wrap; gap:6px; margin:0.5rem 0 1rem 0;">'
    for sk in sorted(found_skills):
        w = job_skill_weights.get(sk, 0)
        html += f"""<span style="
            display:inline-flex; align-items:center; gap:4px;
            padding:0.3rem 0.65rem; border-radius:4px;
            background:{{T['green_dim']}}; border:1px solid {{T['green_border']}};
            color:{{T['green']}}; font-size:0.75rem; font-weight:500;
        ">{{sk.title()}} <span style="opacity:0.6; font-size:0.65rem;">{{w}}</span></span>"""
    for sk in sorted(missing_skills):
        w = job_skill_weights.get(sk, 0)
        html += f"""<span style="
            display:inline-flex; align-items:center; gap:4px;
            padding:0.3rem 0.65rem; border-radius:4px;
            background:{{T['red_dim']}}; border:1px solid {{T['red_border']}};
            color:{{T['red']}}; font-size:0.75rem; font-weight:500;
        ">{{sk.title()}} <span style="opacity:0.6; font-size:0.65rem;">{{w}}</span></span>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def section_divider(T):
    st.markdown(f'<div style="height:1px; background:{{T["border"]}}; margin:2rem 0 1.5rem 0;"></div>',
                unsafe_allow_html=True)


def section_label(text, T):
    st.markdown(f"""<h2 style="
        font-size:0.7rem; font-weight:600; color:{{T['text_tertiary']}};
        text-transform:uppercase; letter-spacing:0.08em;
        margin:0 0 0.75rem 0; padding:0;
    ">{{text}}</h2>""", unsafe_allow_html=True)


def stat_block(label, value, T, color=None):
    c = color or T['text_primary']
    st.markdown(f"""
    <div style="
        padding:1rem; border:1px solid {{T['border']}}; border-radius:6px;
        background:{{T['bg']}};
    ">
        <div style="font-size:0.65rem; font-weight:600; color:{{T['text_tertiary']}};
            text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.35rem;">{{label}}</div>
        <div style="font-size:1.5rem; font-weight:700; color:{{c}};
            letter-spacing:-0.03em; font-family:Inter,sans-serif;">{{value}}</div>
    </div>""", unsafe_allow_html=True)
