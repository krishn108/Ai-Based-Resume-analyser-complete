
import io
import re


# ==========================================
# JOB DATABASE (NO CSV OR SQL DATABASE)
# ==========================================

JOBS = [
    {
        "title": "Python Developer",
        "skills": ["python", "sql", "flask", "git"],
        "description": "Develop Python applications and backend systems."
    },
    {
        "title": "Data Analyst",
        "skills": ["python", "sql", "excel", "pandas", "data analysis"],
        "description": "Analyse data and generate business insights."
    },
    {
        "title": "Machine Learning Intern",
        "skills": ["python", "pandas", "numpy", "machine learning"],
        "description": "Work with data and machine learning models."
    },
    {
        "title": "Web Developer",
        "skills": ["html", "css", "javascript"],
        "description": "Develop and maintain websites."
    },
    {
        "title": "Java Developer",
        "skills": ["java", "sql", "git"],
        "description": "Build software applications using Java."
    },
    {
        "title": "Business Intelligence Intern",
        "skills": ["excel", "sql", "power bi"],
        "description": "Create reports and business dashboards."
    },
    {
        "title": "AI Developer",
        "skills": ["python", "numpy", "machine learning"],
        "description": "Develop artificial intelligence applications."
    },
    {
        "title": "Data Science Intern",
        "skills": [
            "python", "pandas", "numpy",
            "sql", "machine learning", "data analysis"
        ],
        "description": "Explore datasets and develop predictive models."
    }
]


# ==========================================
# KNOWN SKILLS
# ==========================================

KNOWN_SKILLS = sorted(
    set(
        skill
        for job in JOBS
        for skill in job["skills"]
    ),
    key=len,
    reverse=True
)


# ==========================================
# READ PDF AND DOCX RESUMES
# ==========================================

def read_resume(uploaded_file):

    if uploaded_file is None:
        raise ValueError("Please upload a resume.")

    filename = uploaded_file.name.lower()
    file_data = uploaded_file.getvalue()

    if not file_data:
        raise ValueError("The uploaded file is empty.")

    if filename.endswith(".pdf"):

        from pypdf import PdfReader

        try:
            reader = PdfReader(io.BytesIO(file_data))

            if reader.is_encrypted:
                raise ValueError(
                    "PDF is password protected. Upload an unlocked PDF."
                )

            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        except ValueError:
            raise

        except Exception:
            raise ValueError("Unable to read the PDF file.")

    elif filename.endswith(".docx"):

        from docx import Document

        try:
            document = Document(io.BytesIO(file_data))

            parts = []

            for paragraph in document.paragraphs:
                parts.append(paragraph.text)

            for table in document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        parts.append(cell.text)

            text = "\n".join(parts)

        except Exception:
            raise ValueError("Unable to read the DOCX file.")

    else:
        raise ValueError("Only PDF and DOCX files are supported.")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    text = text.strip()

    if not text:
        raise ValueError(
            "No readable text found. Scanned PDFs require OCR."
        )

    return text


# ==========================================
# EXTRACT SKILLS
# ==========================================

def extract_skills(resume_text):

    text = resume_text.lower()
    found_skills = []

    for skill in KNOWN_SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(found_skills)


# ==========================================
# CALCULATE RESUME SCORE
# ==========================================

def calculate_score(resume_text):

    if not KNOWN_SKILLS:
        return 0

    found = extract_skills(resume_text)

    score = round(
        len(found) * 100 / len(KNOWN_SKILLS)
    )

    return max(0, min(100, score))


# ==========================================
# FIND MATCHING JOBS
# ==========================================

def find_matching_jobs(resume_text):

    candidate_skills = extract_skills(resume_text)
    results = []

    for job in JOBS:

        required = job["skills"]

        matched = [
            skill for skill in required
            if skill in candidate_skills
        ]

        missing = [
            skill for skill in required
            if skill not in candidate_skills
        ]

        percentage = round(
            len(matched) * 100 / len(required)
        )

        results.append({
            "title": job["title"],
            "description": job["description"],
            "match": percentage,
            "matched": matched,
            "missing": missing
        })

    results.sort(
        key=lambda item: item["match"],
        reverse=True
    )

    return results


# ==========================================
# SKILL ANALYSIS
# ==========================================

def skill_analysis(resume_text):

    found = extract_skills(resume_text)

    missing = [
        skill for skill in KNOWN_SKILLS
        if skill not in found
    ]

    if len(found) >= 8:
        level = "Good"
        message = "Your resume contains a variety of predefined skills."

    elif len(found) >= 4:
        level = "Intermediate"
        message = "Your resume contains some relevant technical skills."

    else:
        level = "Needs Improvement"
        message = "Consider adding more relevant technical skills."

    suggestions = []

    if not found:
        suggestions.append(
            "Add technical skills that you actually possess."
        )

    if "python" not in found:
        suggestions.append(
            "Consider learning Python for programming and data-related roles."
        )

    if "sql" not in found:
        suggestions.append(
            "Consider learning SQL for database management."
        )

    if "machine learning" not in found:
        suggestions.append(
            "Explore machine learning fundamentals if interested in AI."
        )

    if "git" not in found:
        suggestions.append(
            "Learn Git for version control and project collaboration."
        )

    if not suggestions:
        suggestions.append(
            "Continue developing your existing skills through practical projects."
        )

    return {
        "found": found,
        "missing": missing,
        "level": level,
        "message": message,
        "suggestions": suggestions
    }


# ==========================================
# EXPERIENCE ESTIMATION
# ==========================================

def extract_experience(resume_text):

    text = resume_text.lower()

    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
        text
    )

    if matches:
        return max(float(value) for value in matches)

    return 0


# ==========================================
# GENERATE FULL REPORT
# ==========================================

def generate_report(resume_text, filename):

    score = calculate_score(resume_text)

    skills = skill_analysis(resume_text)

    jobs = find_matching_jobs(resume_text)

    experience = extract_experience(resume_text)

    report = []

    report.append("AI BASED RESUME ANALYSER")
    report.append("=" * 45)

    report.append("\nRESUME INFORMATION")
    report.append("File Name: " + filename)

    report.append("\nRESUME SCORE")
    report.append(str(score) + "%")

    report.append("\nSKILL ANALYSIS")
    report.append("Skill Level: " + skills["level"])

    report.append(
        "Found Skills: "
        + ", ".join(skills["found"])
    )

    report.append(
        "Missing Skills: "
        + ", ".join(skills["missing"])
    )

    report.append("\nEXPERIENCE ESTIMATION")
    report.append(str(experience) + " years")

    report.append("\nJOB MATCHING RESULTS")

    for job in jobs:

        report.append("\n" + job["title"])

        report.append(
            "Match: " + str(job["match"]) + "%"
        )

        report.append(
            "Matched: " + ", ".join(job["matched"])
        )

        report.append(
            "Missing: " + ", ".join(job["missing"])
        )

    report.append("\nIMPROVEMENT SUGGESTIONS")

    for suggestion in skills["suggestions"]:
        report.append("- " + suggestion)

    report.append("\n" + "=" * 45)

    report.append(
        "Note: Scores and job matches are based on predefined "
        "skills and sample job requirements."
    )

    return "\n".join(report)
                  
