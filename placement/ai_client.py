from google import genai


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
