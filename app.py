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
# Function moved inside to bypass Streamlit cache
from placement.exports import create_csv_report, create_pdf_report
from placement.ui_helpers import get_svg_sticker


from google import genai
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from google.genai.errors import ServerError

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(ServerError)
)
def gemini_ai_feedback(resume_text, job_desc, api_key, model="gemini-3.5-flash"):
    client = genai.Client(api_key=api_key)
    prompt = f"""
Resume:
{resume_text}

Job Description:
{job_desc}

Analyze the resume and give clear improvement suggestions.
"""
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text

st.set_page_config(
    page_title="Placement Readiness Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

for key in [
    "resume_text", "matched", "missing",
    "score", "ai_feedback", "analyzed", "job_desc"
]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "analyzed" else False

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    color: #e2e8f0;
}

header {
    background: transparent !important;
}

.st-emotion-cache-16txtl3 {
    padding: 3rem 2rem;
}

/* Sidebar styling for visibility and professional aesthetic */
section[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}
section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] div, 
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
}
section[data-testid="stSidebar"] .stAlert {
    background-color: rgba(255, 255, 255, 0.05) !important;
}

/* Elevate Containers / Cards */
div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.15);
}

/* Premium Buttons */
.stButton>button {
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    border: none !important;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
    color: white !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
}

.stButton>button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
}

/* AI Button */
.main-ai-btn button {
    background: linear-gradient(135deg, #f43f5e 0%, #fb923c 100%) !important;
    font-size: 18px !important;
    padding: 16px 32px !important;
    box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
}

.main-ai-btn button:hover {
    box-shadow: 0 8px 25px rgba(244, 63, 94, 0.5) !important;
}

/* Metrics Styling */
div[data-testid="stMetricValue"] {
    font-weight: 800;
    color: #38bdf8;
    font-size: 2rem;
}
div[data-testid="stMetricLabel"] {
    font-size: 1rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Fix text colors for inputs in dark mode */
.stTextArea textarea {
    color: #ffffff !important;
    background-color: rgba(255,255,255,0.08) !important;
}
div[data-testid="stFileUploader"] {
    color: #ffffff !important;
}
div[data-testid="stFileUploader"] section {
    background-color: rgba(255,255,255,0.08) !important;
}
div[data-testid="stFileUploader"] small, 
div[data-testid="stFileUploader"] span, 
div[data-testid="stFileUploader"] p {
    color: #e2e8f0 !important;
}

p {
    color: #e2e8f0;
}


/* Fix Download Button Text Color */
div[data-testid="stDownloadButton"] button {
    color: #f8fafc !important;
}
div[data-testid="stDownloadButton"] button p {
    color: #f8fafc !important;
}

/* Fix Sidebar Background Override */
[data-testid="stSidebar"] > div:first-child {
    background-color: #0f172a !important;
}
.stSidebar {
    background-color: #0f172a !important;
}


/* Fix File Uploader Button Text */
[data-testid="stFileUploader"] button {
    color: #0f172a !important;
}

/* Force Text Area text to be visible */
[data-testid="stTextArea"] textarea {
    color: #ffffff !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
}
[data-testid="stTextArea"] label {
    color: #f8fafc !important;
}

/* Hide defaults */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


DEFAULT_JOB_DESC = """
We are seeking a motivated and detail-oriented Software Engineer to join our development team. 
The ideal candidate should have strong programming skills in Python and Java, along with a solid 
understanding of Data Structures and Algorithms. Experience with SQL databases, RESTful APIs, 
Git, and Docker is required. Exposure to Machine Learning and Cloud Computing is a plus.
"""

st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Placement Readiness Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 2rem;'>AI-Powered Resume Analysis • Skill Gap Detection • ATS Score</p>", unsafe_allow_html=True)


# --- Sidebar Configuration Panel ---
with st.sidebar:
    st.markdown("### 🎯 How It Works")
    st.markdown("""
    **1. Upload Resume**  
    Drop your PDF resume (text or scanned).
    
    **2. Paste Job Description**  
    Add the details of the job you want.
    
    **3. Run Analysis**  
    Get your ATS match score, identify missing skills, and generate a customized learning timeline!
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ AI Settings")
    
    # Let user select model
    selected_model = st.selectbox(
        "🧠 Select AI Model", 
        ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.1-pro"],
        help="Flash-Lite is fastest. Flash is balanced. Pro is for deep reasoning."
    )
    
    # Try to get secret key, but allow user to override
    default_key = ""
    try:
        default_key = st.secrets.get("GOOGLE_API_KEY", "")
    except Exception:
        pass
        
    api_key_input = st.text_input("🔑 Custom API Key", type="password", help="Paste your own API Key to bypass limits.", value=default_key)
    api_key = api_key_input if api_key_input else default_key
        
    st.markdown("---")
    st.markdown("### 📝 About")
    st.info("This tool uses advanced text extraction and Gemini AI to compare your resume against a job description, helping you identify skill gaps and generate a learning timeline.")

# --- Inputs in Main Page ---
input_col1, input_col2 = st.columns([1, 1], gap="large")

with input_col1:
    st.markdown("### 📄 Upload Resume")
    uploaded_file = st.file_uploader("Drop your PDF here", type=["pdf"])
    st.caption("Supports text-based and scanned PDFs (OCR).")

with input_col2:
    st.markdown("### 🎯 Target Job")
    st.caption("📌 Example Job Description (you can edit or replace this)")
    job_desc = st.text_area("Job Description", value=DEFAULT_JOB_DESC, height=180, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    analyze_clicked = st.button("🔍 Run Full Analysis", width="stretch", key="analyze")


# --- Main Logic ---
if analyze_clicked:
    if uploaded_file:
        with st.spinner("Analyzing resume against job description..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            matched, missing, score = analyze_skills(resume_text, job_desc.lower())

            st.session_state.resume_text = resume_text
            st.session_state.matched = matched
            st.session_state.missing = missing
            st.session_state.score = score
            st.session_state.job_desc = job_desc
            st.session_state.analyzed = True

    else:
        st.warning("Please upload a resume first.")


# --- Ordered Main Results Dashboard ---
if st.session_state.analyzed:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>📊 Analysis Results</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    job_desc_to_use = st.session_state.get("job_desc", job_desc)
    ats_score, matched_keywords = calculate_ats_score(st.session_state.resume_text, job_desc_to_use)

    # 1. METRICS
    metric_cols = st.columns(4)
    metric_cols[0].metric("Readiness Score", f"{st.session_state.score}%")
    metric_cols[1].metric("ATS Match", f"{ats_score}%")
    metric_cols[2].metric("Skills Matched", str(len(st.session_state.matched or [])))
    metric_cols[3].metric("Skills Missing", str(len(st.session_state.missing or [])))

    # 2. PROGRESS BAR
    st.progress(st.session_state.score / 100)
    st.markdown("<br>", unsafe_allow_html=True)

    # 3. EXPORTS
    st.markdown("### 📥 Export Reports")
    csv_bytes = create_csv_report(
        st.session_state.resume_text, job_desc_to_use,
        st.session_state.matched or [], st.session_state.missing or [],
        st.session_state.score, ats_score, st.session_state.ai_feedback or ""
    )
    pdf_bytes = create_pdf_report(
        st.session_state.resume_text, job_desc_to_use,
        st.session_state.matched or [], st.session_state.missing or [],
        st.session_state.score, ats_score, st.session_state.ai_feedback or ""
    )

    d1, d2 = st.columns(2)
    with d1:
        st.download_button("📥 Download CSV Report", data=csv_bytes, file_name="placement_report.csv", mime="text/csv", width="stretch")
    with d2:
        st.download_button("📄 Download PDF Report", data=pdf_bytes, file_name="placement_report.pdf", mime="application/pdf", width="stretch")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 4. MATCHED / MISSING SKILLS
    col1, col2 = st.columns([1, 1])
    with col1:
        st.success("✅ Matched Skills")
        skills = st.session_state.matched
        if skills:
            html = "".join([f'<div style="background-color:rgba(255,255,255,0.05); padding:10px 16px; border-radius:8px; margin-bottom:8px; font-size:15px; border-left: 4px solid #10b981; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display:flex; align-items:center;"><span style="margin-right:8px; font-weight:bold;">•</span>{s.title()}</div>' for s in skills])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.write("None")
    with col2:
        st.error("❌ Missing Skills")
        skills = st.session_state.missing
        if skills:
            html = "".join([f'<div style="background-color:rgba(255,255,255,0.05); padding:10px 16px; border-radius:8px; margin-bottom:8px; font-size:15px; border-left: 4px solid #ef4444; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display:flex; align-items:center;"><span style="margin-right:8px; font-weight:bold;">•</span>{s.title()}</div>' for s in skills])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.write("None")
    st.markdown("<br>", unsafe_allow_html=True)

    # 5. LEARNING TIMELINE
    st.markdown("### 🗓️ Personalized Learning Timeline")
    timeline = learning_timeline(st.session_state.missing)
    if timeline:
        for phase, skills_list in timeline.items():
            st.info(f"**{phase}**  \n{skills_list}")
    else:
        st.success("No critical skill gaps identified! You are well prepared.")
    st.markdown("<br>", unsafe_allow_html=True)

    # 6. ATS MATCH DETAILS EXPANDER
    with st.expander("View Exact Keyword Matches for ATS"):
        if matched_keywords:
            st.write(", ".join(matched_keywords))
        else:
            st.write("No ATS match is found.")
    st.markdown("<br>", unsafe_allow_html=True)

    # 7. SKILL MATCH RADAR
    st.markdown("### 🕸️ Skill Match Radar")
    radar_fig = skill_radar_chart(st.session_state.matched, st.session_state.missing)
    if radar_fig:
        st.plotly_chart(radar_fig, width="stretch")
        
    st.markdown("---")

    # 8. AI-POWERED RESUME FEEDBACK (MAIN FEATURE)
    st.markdown("### ✨ AI-Powered Resume Feedback")
    
    if st.session_state.get('ai_feedback_error'):
        st.error(st.session_state.ai_feedback_error)
    
    if st.session_state.ai_feedback:
        st.markdown(st.session_state.ai_feedback)
    elif api_key:
        st.markdown('<div class="main-ai-btn">', unsafe_allow_html=True)
        if st.button("🤖 Generate Detailed AI Feedback"):
            with st.spinner("Generating insights..."):
                try:
                    from placement.cache import get_cached_feedback, save_feedback
                    cached_response = get_cached_feedback(st.session_state.resume_text, job_desc_to_use)
                    
                    if cached_response:
                        st.session_state.ai_feedback = cached_response
                        st.session_state.ai_feedback_error = None
                    else:
                        # Call API only if not in cache
                        feedback = gemini_ai_feedback(st.session_state.resume_text, job_desc_to_use, api_key, model=selected_model)
                        st.session_state.ai_feedback = feedback
                        st.session_state.ai_feedback_error = None
                        # Save to cache for future runs
                        save_feedback(st.session_state.resume_text, job_desc_to_use, feedback)
                        
                except Exception as e:
                    st.session_state.ai_feedback = None
                    st.session_state.ai_feedback_error = f"AI Error: {str(e)}"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter your Google Gemini API Key in the sidebar to unlock AI feedback.")
