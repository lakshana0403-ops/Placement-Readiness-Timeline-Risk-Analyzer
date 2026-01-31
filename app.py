import streamlit as st
import io
import re
import csv
from placement.extractors import extract_text_from_pdf
from placement.analysis import (
    analyze_skills,
    learning_timeline,
    skill_radar_chart,
    calculate_ats_score,
)
from placement.ai_client import gemini_ai_feedback
from placement.exports import create_csv_report, create_pdf_report
from placement.ui_helpers import get_svg_sticker

st.set_page_config(
    page_title="Placement Readiness Analyzer",
    layout="wide"
)

for key in [
    "resume_text", "matched", "missing",
    "score", "ai_feedback", "analyzed"
]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "analyzed" else False

st.title("🚀 Placement Readiness Analyzer")
st.caption("Resume Analysis • Skill Gap Detection • ATS Score • Gemini AI Feedback")

st.markdown("""
<style>
body {
    font-family: "Segoe UI", Roboto, Arial, sans-serif;
    color: #0f1720;
}
.stMetric {
    padding: 8px 12px;
} 
.stButton>button {
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-weight: 700;
}
.main-analyze-btn button {
    background: linear-gradient(90deg, #0ea5e9, #3b82f6);
    color: white;
    font-size: 16px;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 800;
    width: 100%;
    box-shadow: 0px 6px 20px rgba(59,130,246,0.12);
    transition: all 0.18s ease-in-out;
}
.main-analyze-btn button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 10px 30px rgba(59,130,246,0.18);
}

.main-ai-btn button {
    background: linear-gradient(90deg, #ff1e1e, #ff4d4d);
    color: white;
    font-size: 21px;
    padding: 16px 28px;
    border-radius: 14px;
    font-weight: 800;
    width: 100%;
    box-shadow: 0px 0px 22px rgba(255, 30, 30, 0.7);
    transition: all 0.25s ease-in-out;
}

.main-ai-btn button:hover {
    transform: scale(1.04);
    box-shadow: 0px 0px 32px rgba(255, 30, 30, 1);
}
</style>
""", unsafe_allow_html=True)

# extract_text_from_pdf moved to placement.extractors


# analyze_skills moved to placement.analysis


# learning_timeline moved to placement.analysis


# skill_radar_chart moved to placement.analysis


# calculate_ats_score moved to placement.analysis


# gemini_ai_feedback moved to placement.ai_client

# export helpers moved to placement.exports


DEFAULT_JOB_DESC = """
We are seeking a motivated and detail-oriented Software Engineer to join our development team. 
The ideal candidate should have strong programming skills in Python and Java, along with a solid 
understanding of Data Structures and Algorithms. Experience with SQL databases, RESTful APIs, 
Git, and Docker is required. Exposure to Machine Learning and Cloud Computing is a plus.
"""

st.subheader("🔎 Get Started")
with st.expander("How it works", expanded=False):
    st.write("Upload a resume and paste the job description. Click **Analyze** to generate readiness insights, ATS score, and a personalized learning timeline.")

left, right = st.columns([1, 2])
with left:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    st.caption("Supports text-based and scanned PDFs (OCR).")
with right:
    st.subheader("📝 Paste Job Description")
    st.markdown("<span style='color:#9aa0a6; font-size:13px;'>📌 Example Job Description (you can edit or replace this)</span>", unsafe_allow_html=True)
    job_desc = st.text_area("", value=DEFAULT_JOB_DESC, height=240)
    api_key = st.secrets.get("GOOGLE_API_KEY") or st.text_input("🔑 Google Gemini API Key (optional)", type="password")

btn_container = st.columns([1, 2, 1])
with btn_container[1]:
    st.markdown('<div class="main-analyze-btn">', unsafe_allow_html=True)
    if st.button("🔍 Analyze Resume", use_container_width=True, key="analyze"):
        if uploaded_file:
            with st.spinner("Analyzing resume..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                matched, missing, score = analyze_skills(resume_text, job_desc.lower())

                st.session_state.resume_text = resume_text
                st.session_state.matched = matched
                st.session_state.missing = missing
                st.session_state.score = score
                st.session_state.analyzed = True
        else:
            st.warning("Please upload a resume.")
    st.markdown('</div>', unsafe_allow_html=True) 

if st.session_state.analyzed:
    st.divider()
    st.subheader("📊 Placement Readiness Result")

    k1, k2, k3, k4 = st.columns(4)
    ats_score, matched_keywords = calculate_ats_score(
        st.session_state.resume_text, job_desc
    )
    k1.metric("Readiness", f"{st.session_state.score}%")
    k2.metric("ATS Score", f"{ats_score}%")
    k3.metric("Matched Skills", str(len(st.session_state.matched or [])))
    k4.metric("Missing Skills", str(len(st.session_state.missing or [])))

    st.progress(st.session_state.score / 100)

    csv_bytes = create_csv_report(
        st.session_state.resume_text,
        job_desc,
        st.session_state.matched or [],
        st.session_state.missing or [],
        st.session_state.score,
        ats_score,
        st.session_state.ai_feedback or ""
    )

    pdf_bytes = create_pdf_report(
        st.session_state.resume_text,
        job_desc,
        st.session_state.matched or [],
        st.session_state.missing or [],
        st.session_state.score,
        ats_score,
        st.session_state.ai_feedback or ""
    )

    d1, d2 = st.columns([1, 1])
    with d1:
        st.download_button("📥 Download CSV Report", data=csv_bytes, file_name="placement_report.csv", mime="text/csv")
    with d2:
        st.download_button("📄 Download PDF Report", data=pdf_bytes, file_name="placement_report.pdf", mime="application/pdf")

    st.markdown(get_svg_sticker(), unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.success("✅ Matched Skills")
        st.write(st.session_state.matched or "None")
    with col2:
        st.error("❌ Missing Skills")
        st.write(st.session_state.missing or "None")

    st.subheader("🗓️ Personalized Learning Timeline")
    timeline = learning_timeline(st.session_state.missing)
    for week, (skill, reason) in timeline.items():
        st.info(f"**{week}: {skill}**  \n📌 {reason}")

    st.subheader("📊 ATS Match Details")
    with st.expander("✅ Matched Keywords"):
        st.write(", ".join(matched_keywords))

    radar_fig = skill_radar_chart(
        st.session_state.matched,
        st.session_state.missing
    )
    if radar_fig:
        st.subheader("🕸️ Skill Match Radar")
        st.plotly_chart(radar_fig, use_container_width=True)

st.divider()
st.subheader("✨ AI-Powered Resume Feedback (Main Feature)")
st.markdown(
    "<p style='color:#9aa0a6;'>Uses <b>Google Gemini AI</b> for deep resume analysis</p>",
    unsafe_allow_html=True
)

if api_key and st.session_state.analyzed:
    st.markdown('<div class="main-ai-btn">', unsafe_allow_html=True)
    if st.button("🤖 Get Gemini AI Feedback"):
        with st.spinner("Generating Gemini AI feedback..."):
            st.session_state.ai_feedback = gemini_ai_feedback(
                st.session_state.resume_text, job_desc, api_key
            )
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.ai_feedback:
    st.divider()
    st.subheader("🧠 Gemini AI Feedback")
    st.markdown(st.session_state.ai_feedback)
