from google import genai
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from google.genai.errors import ServerError

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(ServerError)
)
def gemini_ai_feedback(resume_text, job_desc, api_key, model="gemini-3.8-flash"):
    client = genai.Client(api_key=api_key)
    prompt = f"""
Resume:
{resume_text}

Job Description:
{job_desc}

Analyze the resume and give clear improvement suggestions.
"""
    # Changed model to gemini-3.8-flash for more stability and added tenacity retry logic
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text
