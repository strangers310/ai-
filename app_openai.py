import os
import json
import requests
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="AI Resume Optimizer - OpenAI")
templates = Jinja2Templates(directory="templates")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def call_llm_for_resume_analysis(jd_text: str, resume_text: str):
    if not OPENAI_API_KEY:
        return {
            "summary": "OPENAI_API_KEY is not configured yet. Add it to your environment before running the real model version.",
            "matched": [],
            "missing": ["Python", "FastAPI", "Prompt Engineering", "LLM", "Agent"],
            "rewrite": [
                "Built an AI-powered web prototype for resume-job matching.",
                "Integrated a backend service with prompt-based content generation.",
                "Improved resume alignment through keyword analysis and targeted rewriting."
            ]
        }

    system_prompt = (
        "You are an AI resume optimization assistant. "
        "Analyze the job description and resume content, then return strictly valid JSON with these keys: "
        "summary (string), matched (array of strings), missing (array of strings), rewrite (array of 3 concise resume bullet suggestions)."
    )

    user_prompt = f"""
Job Description:
{jd_text}

Resume Content:
{resume_text}
"""

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"}
    }

    response = requests.post(
        f"{OPENAI_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    return {
        "summary": parsed.get("summary", "No summary returned."),
        "matched": parsed.get("matched", []),
        "missing": parsed.get("missing", []),
        "rewrite": parsed.get("rewrite", []),
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


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
        "index.html",
        {
            "request": request,
            "result": result,
            "jd_text": jd_text,
            "resume_text": resume_text,
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}
