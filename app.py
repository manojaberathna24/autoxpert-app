import os
import json
from io import BytesIO
from typing import Optional, Dict, Any, Tuple

import streamlit as st

from utils.openrouter_client import call_openrouter_json
from utils.file_utils import extract_text_from_upload


st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="💼",
    layout="wide",
)


def get_api_key() -> Optional[str]:
    # Prefer Streamlit secrets, fallback to environment variable
    if "OPENROUTER_API_KEY" in st.secrets:
        return st.secrets["OPENROUTER_API_KEY"]
    return os.getenv("OPENROUTER_API_KEY")


def analyze_application(
    cv_text: str, job_text: str, skills_text: str, model: str
) -> Dict[str, Any]:
    system_prompt = (
        "You are an expert career coach and ATS (Applicant Tracking System) specialist. "
        "Given a candidate's CV, a job description, and a list of skills, you must:\n"
        "1. Evaluate the ATS match between the CV and the job description.\n"
        "2. Identify concrete skill gaps and missing keywords.\n"
        "3. Rewrite the CV in a clear, concise, and ATS-optimized way (no tables, keep it text-only).\n"
        "4. Draft a tailored, professional cover letter.\n\n"
        "Return ONLY valid JSON with the following keys:\n"
        "- ats_score: integer from 0 to 100\n"
        "- ats_feedback: string, a few bullet-style points explaining the score\n"
        "- skill_gaps: array of strings describing missing or weak skills/keywords\n"
        "- improved_cv: string, a complete improved CV text\n"
        "- cover_letter: string, a complete custom cover letter\n"
    )

    user_prompt = {
        "cv": cv_text,
        "job_description": job_text,
        "skills": skills_text,
    }

    return call_openrouter_json(
        system_prompt=system_prompt,
        user_payload=user_prompt,
        model=model,
    )


def build_download_docx_bytes(text: str, title: str) -> BytesIO:
    from docx import Document

    doc = Document()
    for line in text.splitlines():
        doc.add_paragraph(line if line.strip() != "" else "")
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def build_download_pdf_bytes(text: str, title: str) -> BytesIO:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x_margin = 50
    y = height - 50
    max_width = width - 2 * x_margin
    text_object = c.beginText(x_margin, y)

    # Simple wrapping by characters
    max_chars = 95
    for line in text.splitlines():
        while len(line) > max_chars:
            text_object.textLine(line[:max_chars])
            line = line[max_chars:]
        text_object.textLine(line)
    c.drawText(text_object)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def main():
    st.title("💼 AI Job Application Assistant")
    st.write(
        "Upload your CV and job description, list your skills, and let the AI generate "
        "an ATS score, skill gap analysis, an improved CV, and a tailored cover letter."
    )

    api_key = get_api_key()
    if not api_key:
        st.warning(
            "No OpenRouter API key detected. Set `OPENROUTER_API_KEY` as an environment variable "
            "or in `.streamlit/secrets.toml` to use the assistant."
        )

    with st.sidebar:
        st.subheader("Settings")
        model = st.selectbox(
            "OpenRouter model",
            [
                "openai/gpt-4.1-mini",
                "openai/gpt-4.1",
                "openai/gpt-4o-mini",
                "anthropic/claude-3.5-sonnet",
            ],
            index=0,
            help="Choose an OpenRouter-compatible GPT-4/5-level model.",
        )
        st.markdown(
            "You must have an OpenRouter API key configured to make requests.\n\n"
            "More info: `https://openrouter.ai`"
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. CV Upload")
        cv_file = st.file_uploader(
            "Upload your CV (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"]
        )
        cv_text_manual = st.text_area(
            "Or paste your CV text",
            height=200,
            placeholder="Paste your CV here if you don't want to upload a file...",
        )

    with col2:
        st.subheader("2. Job Description")
        jd_file = st.file_uploader(
            "Upload job description (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"]
        )
        jd_text_manual = st.text_area(
            "Or paste the job description",
            height=200,
            placeholder="Paste the job description here...",
        )

    st.subheader("3. Skills")
    skills_text = st.text_area(
        "List your skills (comma-separated or one per line)",
        height=120,
        placeholder="e.g. Python, Machine Learning, SQL, AWS, Docker...",
    )

    analyze_clicked = st.button("🚀 Analyze & Generate Documents", type="primary")

    if analyze_clicked:
        if not api_key:
            st.error("OpenRouter API key is required to run the analysis.")
            st.stop()

        with st.spinner("Reading files and preparing prompts..."):
            cv_text = extract_text_from_upload(cv_file) if cv_file else ""
            jd_text = extract_text_from_upload(jd_file) if jd_file else ""

            if not cv_text and not cv_text_manual.strip():
                st.error("Please upload a CV or paste your CV text.")
                st.stop()
            if not jd_text and not jd_text_manual.strip():
                st.error("Please upload a job description or paste it.")
                st.stop()

            cv_full = cv_text_manual.strip() or cv_text
            jd_full = jd_text_manual.strip() or jd_text

        with st.spinner("Calling OpenRouter and generating results..."):
            try:
                result = analyze_application(cv_full, jd_full, skills_text, model)
            except Exception as e:
                st.error(f"Error while calling OpenRouter: {e}")
                st.stop()

        ats_score = result.get("ats_score")
        ats_feedback = result.get("ats_feedback", "")
        skill_gaps = result.get("skill_gaps", [])
        improved_cv = result.get("improved_cv", "")
        cover_letter = result.get("cover_letter", "")

        st.success("Analysis complete!")

        top_col1, top_col2 = st.columns(2)
        with top_col1:
            st.metric("ATS Score", f"{ats_score if ats_score is not None else 'N/A'} / 100")
        with top_col2:
            st.write("**ATS Feedback**")
            st.markdown(ats_feedback or "_No feedback provided_")

        st.subheader("Skill Gap Analysis")
        if skill_gaps:
            for gap in skill_gaps:
                st.markdown(f"- {gap}")
        else:
            st.markdown("_No specific skill gaps identified._")

        st.subheader("Improved CV (AI-generated)")
        st.text_area("Improved CV", improved_cv, height=350)

        st.subheader("Custom Cover Letter (AI-generated)")
        st.text_area("Cover Letter", cover_letter, height=350)

        # Build downloads
        if improved_cv:
            cv_docx = build_download_docx_bytes(improved_cv, "Improved CV")
            cv_pdf = build_download_pdf_bytes(improved_cv, "Improved CV")

            st.markdown("**Download Improved CV:**")
            st.download_button(
                "Download CV as DOCX",
                data=cv_docx,
                file_name="improved_cv.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            st.download_button(
                "Download CV as PDF",
                data=cv_pdf,
                file_name="improved_cv.pdf",
                mime="application/pdf",
            )

        if cover_letter:
            cl_docx = build_download_docx_bytes(cover_letter, "Cover Letter")
            cl_pdf = build_download_pdf_bytes(cover_letter, "Cover Letter")

            st.markdown("**Download Cover Letter:**")
            st.download_button(
                "Download Cover Letter as DOCX",
                data=cl_docx,
                file_name="cover_letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            st.download_button(
                "Download Cover Letter as PDF",
                data=cl_pdf,
                file_name="cover_letter.pdf",
                mime="application/pdf",
            )


if __name__ == "__main__":
    main()

import streamlit as st
import requests
import json
from PIL import Image
import io
import base64
from pages import home, damage_detection, tire_analysis, market_price, feedback

# Page configuration
st.set_page_config(
    page_title="AutoXpert - Smart Vehicle Solutions",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
    .stApp > header {
        display: none;
    }
    footer {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Professional Global CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        padding: 0;
    }
    
    .stApp {
        background: #f8f9fa;
    }
    
    /* Professional Button Styles */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Professional Input Styles */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border: 1.5px solid #e0e0e0;
        border-radius: 8px;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Professional Card Styles */
    .professional-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e8e8e8;
        transition: all 0.3s;
    }
    
    .professional-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Professional Navigation */
    .nav-button {
        background: #ffffff;
        border: 1.5px solid #e0e0e0;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .nav-button:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Navigation handler
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

# Main app routing
if st.session_state.current_page == 'home':
    home.show()
elif st.session_state.current_page == 'damage':
    damage_detection.show()
elif st.session_state.current_page == 'tire':
    tire_analysis.show()
elif st.session_state.current_page == 'market':
    market_price.show()
elif st.session_state.current_page == 'feedback':
    feedback.show()
