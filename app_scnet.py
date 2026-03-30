import os
import json
from openai import OpenAI
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AI Resume Optimizer - SCNet MiniMax")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.scnet.cn/api/llm/v1")
MODEL = os.getenv("OPENAI_MODEL", "MiniMax-M2.5")


def create_client():
    return OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )


def call_llm_for_resume_analysis(jd_text: str, resume_text: str):
    if not API_KEY:
        return {
            "summary": "OPENAI_API_KEY is not configured yet.",
            "matched": [],
            "missing": ["Python", "FastAPI", "Prompt Engineering", "LLM", "Agent"],
            "rewrite": [
                "Built an AI-powered web prototype for resume-job matching.",
                "Integrated a backend service with prompt-based content generation.",
                "Improved resume alignment through keyword analysis and targeted rewriting."
            ]
        }

    client = create_client()

    system_prompt = (
        "You are an AI resume optimization assistant. "
        "Analyze the job description and resume content. "
        "Return strictly valid JSON only, with these keys: "
        "summary (string), matched (array of strings), missing (array of strings), "
        "rewrite (array of 3 concise resume bullet suggestions). "
        "Do not return markdown. Do not return explanations outside JSON."
    )

    user_prompt = f"""
Job Description:
{jd_text}

Resume Content:
{resume_text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1024,
        temperature=0.3,
        stream=False
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return {
            "summary": f"Model returned non-JSON content: {content}",
            "matched": [],
            "missing": [],
            "rewrite": [],
        }

    return {
        "summary": parsed.get("summary", "No summary returned."),
        "matched": parsed.get("matched", []),
        "missing": parsed.get("missing", []),
        "rewrite": parsed.get("rewrite", []),
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": None,
            "jd_text": "",
            "resume_text": "",
        },
    )


@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, jd_text: str = Form(...), resume_text: str = Form(...)):
    try:
        result = call_llm_for_resume_analysis(jd_text, resume_text)
    except Exception as e:
        result = {
            "summary": f"Request failed: {str(e)}",
            "matched": [],
            "missing": [],
            "rewrite": [],
        }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": result,
            "jd_text": jd_text,
            "resume_text": resume_text,
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}