import streamlit as st
import io
import re
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
from google import genai
import plotly.graph_objects as go

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Placement Readiness Analyzer",
    layout="wide"
)

st.title("🚀 Placement Readiness Analyzer")
st.caption("Resume Analysis • Skill Gap Detection • ATS Score • Gemini AI Feedback")

# ===================== SESSION STATE =====================
for key in [
    "resume_text", "matched", "missing",
    "score", "ai_feedback", "analyzed"
]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "analyzed" else False

# ===================== STYLES =====================
st.markdown("""
<style>
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

# ===================== FUNCTIONS =====================
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_bytes = pdf_file.read()
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            text += page.extract_text() or ""
    except:
        pass

    if not text.strip():
        images = convert_from_bytes(pdf_bytes)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text.lower()


def analyze_skills(resume_text, job_desc):
    skills = [
        "python", "java", "sql", "data structures", "algorithms",
        "git", "docker", "rest api", "machine learning", "cloud computing"
    ]

    matched, missing = [], []

    for skill in skills:
        if skill in job_desc:
            if skill in resume_text:
                matched.append(skill)
            else:
                missing.append(skill)

    score = int((len(matched) / max(len(matched) + len(missing), 1)) * 100)
    return matched, missing, score


def learning_timeline(missing):
    order = [
        ("python", "Foundation language"),
        ("java", "OOP concepts"),
        ("data structures", "Problem solving"),
        ("algorithms", "Interview readiness"),
        ("sql", "Database handling"),
        ("rest api", "Backend integration"),
        ("git", "Version control"),
        ("docker", "Deployment skills"),
        ("machine learning", "Advanced analytics"),
        ("cloud computing", "Scalable deployment")
    ]

    timeline = {}
    week = 1
    for skill, reason in order:
        if skill in missing:
            timeline[f"Week {week}"] = (skill.title(), reason)
            week += 1
    return timeline


def skill_radar_chart(matched, missing):
    if not matched and not missing:
        return None

    skills = matched + missing
    values = [1 if s in matched else 0 for s in skills]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=skills + [skills[0]],
        fill="toself"
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        height=420
    )
    return fig


def calculate_ats_score(resume_text, job_desc):
    jd_words = set(re.findall(r"[a-zA-Z]{3,}", job_desc.lower()))
    resume_words = set(re.findall(r"[a-zA-Z]{3,}", resume_text.lower()))
    matched = jd_words.intersection(resume_words)
    score = (len(matched) / len(jd_words)) * 100 if jd_words else 0
    return round(score, 2), sorted(matched)


def gemini_ai_feedback(resume_text, job_desc, api_key):
    client = genai.Client(api_key=api_key)
    prompt = f"""
Resume:
{resume_text}

Job Description:
{job_desc}

Analyze the resume and give clear improvement suggestions.
"""
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    return response.text

# ===================== DEFAULT JOB DESCRIPTION =====================
DEFAULT_JOB_DESC = """
We are seeking a motivated and detail-oriented Software Engineer to join our development team. 
The ideal candidate should have strong programming skills in Python and Java, along with a solid 
understanding of Data Structures and Algorithms. Experience with SQL databases, RESTful APIs, 
Git, and Docker is required. Exposure to Machine Learning and Cloud Computing is a plus.
"""

# ===================== INPUT SECTION =====================
st.subheader("📄 Upload Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

st.subheader("📝 Paste Job Description")
st.markdown(
    "<span style='color:#9aa0a6; font-size:13px;'>📌 Example Job Description (you can edit or replace this)</span>",
    unsafe_allow_html=True
)

job_desc = st.text_area("", value=DEFAULT_JOB_DESC, height=240)

api_key = st.secrets.get("GOOGLE_API_KEY") or st.text_input(
    "🔑 Enter Google Gemini API Key",
    type="password"
)

# ===================== ANALYZE BUTTON =====================
if st.button("🔍 Analyze Resume", use_container_width=True):
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

# ===================== RESULTS =====================
if st.session_state.analyzed:
    st.divider()
    st.subheader("📊 Placement Readiness Result")

    st.progress(st.session_state.score / 100)
    st.metric("Readiness Score", f"{st.session_state.score}%")

    col1, col2 = st.columns(2)
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

    ats_score, matched_keywords = calculate_ats_score(
        st.session_state.resume_text, job_desc
    )

    st.subheader("📊 ATS Match Score")
    st.progress(ats_score / 100)
    st.write(f"**ATS Score:** {ats_score}%")

    with st.expander("✅ Matched Keywords"):
        st.write(", ".join(matched_keywords))

    radar_fig = skill_radar_chart(
        st.session_state.matched,
        st.session_state.missing
    )
    if radar_fig:
        st.subheader("🕸️ Skill Match Radar")
        st.plotly_chart(radar_fig, use_container_width=True)

# ===================== GEMINI AI (MAIN FEATURE) =====================
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
