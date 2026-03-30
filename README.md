# AI Resume Optimizer

An AI-powered resume optimization web app for analyzing job descriptions and improving resume content.

## Overview

AI Resume Optimizer helps users compare their resume against a target job description and receive structured optimization suggestions.

The app supports:
- job description analysis
- keyword matching
- missing skill identification
- resume bullet rewrite suggestions

This project is built as an AI product prototype for internship applications in AI product, LLM application, and agent-oriented roles.

## Demo Features

- Paste a target **Job Description**
- Paste your current **Resume Content**
- Generate:
  - **Analysis Summary**
  - **Matched Keywords**
  - **Missing Keywords**
  - **Suggested Resume Bullets**

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Model API:** National Supercomputing Platform API
- **LLM Model:** MiniMax-M2.5
- **Libraries:** openai, requests, jinja2
- **Tools:** Git, GitHub

## Project Structure

```bash
AI-Resume-Optimizer/
├── README.md
├── requirements.txt
├── app.py
├── app_scnet.py
├── .env.example
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## How It Works

The application takes a job description and resume text as input, sends them to an LLM with a structured prompt, and requests a JSON-formatted response containing:

- summary
- matched keywords
- missing keywords
- rewritten resume bullets

The backend then parses the result and renders it in a simple web interface.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/kieran-He/AI-Resume-Optimizer.git
cd AI-Resume-Optimizer
```

### 2. Create and activate a Conda environment

```bash
conda create -n ai-resume python=3.11
conda activate ai-resume
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
export OPENAI_API_KEY="your_scnet_api_key"
export OPENAI_BASE_URL="https://api.scnet.cn/api/llm/v1"
export OPENAI_MODEL="MiniMax-M2.5"
```

### 5. Run the app

```bash
uvicorn app_scnet:app --reload
```

Then open:

```bash
http://127.0.0.1:8000
```

## Example Use Case

**Input**
- A target JD for an AI product or LLM-related internship
- A draft resume

**Output**
- High-level fit analysis
- matched skills
- missing skills
- optimized resume bullet suggestions

## Example Output

- **Analysis Summary**  
  The candidate has foundational Python skills and some exposure to API integration and LLM applications, but lacks specific experience in FastAPI, prompt engineering, web prototyping, and agent workflow design.

- **Matched Keywords**
  - Python
  - API integration
  - LLM-based applications

- **Missing Keywords**
  - FastAPI
  - Prompt engineering
  - Web prototyping
  - Agent workflow design

- **Suggested Resume Bullets**
  - Built backend services using Python and integrated REST APIs for small-scale applications
  - Developed web prototypes with HTML/CSS/JavaScript for user testing and feedback
  - Experimented with LLM prompt engineering to optimize model outputs for specific use cases

## Project Highlights

- Built an end-to-end AI web application from scratch
- Integrated an external LLM API into a FastAPI-based backend
- Designed structured prompts for resume-job matching
- Converted model outputs into a usable product interface
- Demonstrated practical AI application development for a real user scenario

## Resume Description

**AI Resume Optimizer | Independent Project**
- Built a web-based AI resume optimization tool using FastAPI and a lightweight frontend
- Integrated the National Supercomputing Platform MiniMax-M2.5 API for job description analysis and resume rewriting
- Designed structured prompts to generate keyword matching, gap analysis, and optimized resume bullets
- Developed a functional prototype to validate LLM applications in job-search scenarios

## Future Improvements

- support PDF resume upload
- support Chinese and English job descriptions
- add copy-to-clipboard for generated bullets
- generate a fully revised resume section
- improve prompt robustness and output formatting

## License

This project is for learning and portfolio use.
