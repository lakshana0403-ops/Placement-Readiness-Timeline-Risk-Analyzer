import re
import plotly.graph_objects as go


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
