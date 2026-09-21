import re
import plotly.graph_objects as go

# Comprehensive List of Tech Skills
import json
import os

# Load skills dynamically from external configuration file
data_path = os.path.join(os.path.dirname(__file__), "skills_data.json")
try:
    with open(data_path, "r") as f:
        _data = json.load(f)
        TECH_SKILLS = _data.get("TECH_SKILLS", [])
        SKILL_DB = _data.get("SKILL_DB", {})
except Exception:
    TECH_SKILLS = []
    SKILL_DB = {}

def analyze_skills(resume_text, job_desc):
    matched, missing = [], []
    
    # Pad texts with spaces to make edge-matching easier
    job_desc_padded = " " + job_desc.lower().replace('\n', ' ') + " "
    resume_text_padded = " " + resume_text.lower().replace('\n', ' ') + " "
    
    for skill in TECH_SKILLS:
        skill_lower = skill.lower()
        
        # Use regex to match the skill only if it is a distinct word (not surrounded by other letters)
        # We use a lookbehind and lookahead to ensure the skill isn't inside another word (e.g. "go" inside "algorithm")
        pattern = r"(?<![a-z])" + re.escape(skill_lower) + r"(?![a-z])"
        
        if re.search(pattern, job_desc_padded):
            if re.search(pattern, resume_text_padded):
                matched.append(skill)
            else:
                missing.append(skill)

    score = int((len(matched) / max(len(matched) + len(missing), 1)) * 100)
    return matched, missing, score


def learning_timeline(missing):
    phases = {
        "Phase 1: Core Fundamentals": {"time": "1-4 Weeks", "skills": []},
        "Phase 2: Problem Solving": {"time": "4-8 Weeks", "skills": []},
        "Phase 3: Backend & Integration": {"time": "2-4 Weeks", "skills": []},
        "Phase 4: Frontend & UI": {"time": "2-4 Weeks", "skills": []},
        "Phase 5: Databases & Storage": {"time": "2-3 Weeks", "skills": []},
        "Phase 6: Deployment & DevOps": {"time": "2-4 Weeks", "skills": []},
        "Phase 7: Advanced Topics (ML/Data)": {"time": "8-12+ Weeks", "skills": []}
    }
    
    skill_db = SKILL_DB

    for skill in missing:
        skill_lower = skill.lower()
        if skill_lower in skill_db:
            phase_name, reason = skill_db[skill_lower]
            phases[phase_name]["skills"].append(f"✅ **{skill.title()}**: {reason}")
        else:
            # Fallback for dynamic skills not strictly in the DB
            phases["Phase 1: Core Fundamentals"]["skills"].append(f"✅ **{skill.title()}**: Self-guided learning")
    
    timeline = {}
    for phase_name, data in phases.items():
        if data["skills"]:
            key = f"{phase_name} (⏳ {data['time']})"
            skills_text = "\n\n".join(data["skills"])
            timeline[key] = skills_text
            
    return timeline


def skill_radar_chart(matched, missing):
    if not matched and not missing:
        return None

    # Limit radar chart to top 12 skills max for visual clarity
    skills = (matched + missing)[:12]
    values = [1 if s in matched else 0 for s in skills]
    
    # If there are no skills to display, don't crash
    if not skills:
        return None

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
    import re
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Text preprocessing
    def preprocess(text):
        text = text.lower()
        # Remove non-alphanumeric characters
        text = re.sub(r'[^a-z0-9\s]', '', text)
        return text
        
    doc1 = preprocess(resume_text)
    doc2 = preprocess(job_desc)
    
    # If empty texts
    if not doc1 or not doc2:
        return 0.0, []
        
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([doc2, doc1])  # JD is index 0, Resume is index 1
        
        # Calculate cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = float(cosine_sim[0][0]) * 100
        
        # Extract matched keywords (words present in both vectors, excluding common english words)
        feature_names = vectorizer.get_feature_names_out()
        doc1_vector = tfidf_matrix[1].toarray()[0]
        doc2_vector = tfidf_matrix[0].toarray()[0]
        
        matched_keywords = []
        for i, feature in enumerate(feature_names):
            if doc1_vector[i] > 0 and doc2_vector[i] > 0:
                matched_keywords.append(feature)
                
        return round(score, 2), sorted(matched_keywords)
    except Exception:
        return 0.0, []
