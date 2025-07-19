from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from resume_generator import generate_pdf
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def render_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def create_resume(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    city: str = Form(...),
    github: str = Form(...),
    linkedin: str = Form(...),
    objective: str = Form(...),
    languages: str = Form(...),
    frontend: str = Form(...),
    backend: str = Form(...),
    databases: str = Form(...),
    cloud: str = Form(...),
    project_name: List[str] = Form(...),
    project_description: List[str] = Form(...),
    project_technologies: List[str] = Form(...),
    project_link: List[str] = Form(...),
    degree: List[str] = Form(...),
    institute: List[str] = Form(...),
    year: List[str] = Form(...),
    grade: List[str] = Form(...),
    company: List[str] = Form(...),
    role: List[str] = Form(...),
    duration: List[str] = Form(...),
    responsibilities: List[str] = Form(...),
    technologies: List[str] = Form(...),
    achievements: List[str] = Form(default=[])
):
    # Work Experience
    work_history = []
    for idx in range(len(company)):
        if company[idx].strip():
            entry = {
                "company": company[idx],
                "role": role[idx],
                "duration": duration[idx],
                "responsibilities": [line.strip() for line in responsibilities[idx].split('\n') if line.strip()],
                "technologies": technologies[idx]
            }
            work_history.append(entry)

    # Projects
    project_list = []
    for idx in range(len(project_name)):
        if project_name[idx].strip():
            project_list.append({
                "name": project_name[idx],
                "description": project_description[idx],
                "technologies": project_technologies[idx],
                "link": project_link[idx]
            })

    # Education
    academic_history = []
    for idx in range(len(degree)):
        if degree[idx].strip():
            academic_history.append({
                "degree": degree[idx],
                "institute": institute[idx],
                "year": year[idx],
                "grade": grade[idx]
            })

    # Collecting all information
    final_resume = {
        "name": name,
        "email": email,
        "phone": phone,
        "city": city,
        "github": github,
        "linkedin": linkedin,
        "objective": objective,
        "skills": {
            "programming_languages": [item.strip() for item in languages.split(',')],
            "tools_and_frameworks": [item.strip() for item in frontend.split(',')],
            "devops_tools": [item.strip() for item in backend.split(',')],
            "databases": [item.strip() for item in databases.split(',')],
            "cloud_platforms": [item.strip() for item in cloud.split(',')]
        },
        "experience": work_history,
        "projects": project_list,
        "education": academic_history,
        "achievements": [note.strip() for note in achievements if note.strip()]
    }

    result_pdf = generate_pdf(final_resume)
    return FileResponse(result_pdf, filename=result_pdf, media_type="application/pdf")
