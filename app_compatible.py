import os
import json
import requests
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AI Resume Optimizer - Compatible API")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")
APP_TITLE = os.getenv("APP_TITLE", "AI Resume Optimizer")


def call_llm_for_resume_analysis(jd_text: str, resume_text: str):
    if not API_KEY:
        return {
            "summary": "API key is not configured yet. Add OPENAI_API_KEY before running the compatible model version.",
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
        "summary (string), matched (array of strings), missing (array of strings), "
        "rewrite (array of 3 concise resume bullet suggestions)."
    )

    user_prompt = f"""
Job Description:
{jd_text}

Resume Content:
{resume_text}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"}
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    if "openrouter.ai" in BASE_URL:
        headers["HTTP-Referer"] = "http://localhost:8000"
        headers["X-Title"] = APP_TITLE

    response = requests.post(
        f"{BASE_URL.rstrip('/')}/chat/completions",
        headers=headers,
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
