from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="AI Resume Optimizer")
templates = Jinja2Templates(directory="templates")


def build_demo_result(jd_text: str, resume_text: str):
    jd_keywords = [
        "Python", "FastAPI", "Prompt Engineering", "LLM", "Agent", "HTML", "API"
    ]
    matched = [kw for kw in jd_keywords if kw.lower() in resume_text.lower()]
    missing = [kw for kw in jd_keywords if kw.lower() not in resume_text.lower()]

    return {
        "summary": "This is a demo analysis result. Replace this logic with a real LLM API call.",
        "matched": matched,
        "missing": missing,
        "rewrite": [
            "Built an AI-enabled product prototype with a lightweight web frontend and backend integration.",
            "Used Python-based services and structured prompts to support analysis and content generation.",
            "Improved resume alignment for target job descriptions through keyword extraction and rewrite suggestions."
        ]
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, jd_text: str = Form(...), resume_text: str = Form(...)):
    result = build_demo_result(jd_text, resume_text)
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
