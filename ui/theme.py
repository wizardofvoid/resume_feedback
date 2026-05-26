import streamlit as st

def get_theme_tokens():
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    is_dark = st.session_state.theme == "dark"

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
    return T, is_dark


def setup_theme(T, is_dark):
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
