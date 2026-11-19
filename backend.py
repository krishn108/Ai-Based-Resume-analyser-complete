
import io
import re


# ==========================================
# 1. SAMPLE JOB DATABASE
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
        "description": "Analyse datasets and generate useful insights."
    },
    {
        "title": "Machine Learning Intern",
        "skills": ["python", "pandas", "numpy", "machine learning"],
        "description": "Work with datasets and machine learning models."
    },
    {
        "title": "Web Developer",
        "skills": ["html", "css", "javascript", "git"],
        "description": "Develop and maintain web applications."
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
        "skills": ["python", "numpy", "machine learning", "tensorflow"],
        "description": "Develop artificial intelligence applications."
    },
    {
        "title": "Data Science Intern",
        "skills": [
            "python", "pandas", "numpy",
            "sql", "machine learning", "data analysis"
        ],
        "description": "Explore datasets and develop predictive models."
    },
    {
        "title": "Database Developer",
        "skills": ["sql", "mysql", "database", "python"],
        "description": "Design and manage database systems."
    },
    {
        "title": "Software Developer",
        "skills": ["python", "java", "git", "sql"],
        "description": "Develop and maintain software applications."
    }
]


# ==========================================
# 2. SKILL DATABASE
# ==========================================

KNOWN_SKILLS = [
    "machine learning",
    "data analysis",
    "power bi",
    "javascript",
    "tensorflow",
    "scikit-learn",
    "artificial intelligence",
    "deep learning",
    "computer vision",
    "data science",
    "programming",
    "database",
    "mysql",
    "mongodb",
    "flask",
    "django",
    "streamlit",
    "pandas",
    "numpy",
    "excel",
    "python",
    "java",
    "c++",
    "c programming",
    "sql",
    "html",
    "css",
    "git",
    "github",
    "react",
    "communication",
    "leadership",
    "problem solving",
    "teamwork"
]

KNOWN_SKILLS = sorted(
    set(KNOWN_SKILLS),
    key=len,
    reverse=True
)


# ==========================================
# 3. READ PDF AND DOCX
# ==========================================

def read_resume(uploaded_file):

    if uploaded_file is None:
        raise ValueError("Please select a resume.")

    filename = uploaded_file.name.lower()

    file_data = uploaded_file.getvalue()

    if not file_data:
        raise ValueError("The selected file is empty.")

    if len(file_data) > 10 * 1024 * 1024:
        raise ValueError("File size must be below 10 MB.")

    if filename.endswith(".pdf"):

        from pypdf import PdfReader

        try:
            reader = PdfReader(io.BytesIO(file_data))

            if reader.is_encrypted:
                raise ValueError(
                    "This PDF is password protected. "
                    "Please upload an unlocked PDF."
                )

            extracted_parts = []

            for page in reader.pages:
                extracted_parts.append(
                    page.extract_text() or ""
                )

            text = "\n".join(extracted_parts)

        except ValueError:
            raise

        except Exception:
            raise ValueError(
                "Unable to read PDF. Please try another PDF file."
            )

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
            raise ValueError(
                "Unable to read DOCX. Please check the document."
            )

    else:

        raise ValueError(
            "Unsupported file format. Select PDF or DOCX."
        )

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    text = text.strip()

    if not text:
        raise ValueError(
            "No readable text found. Scanned PDFs require OCR."
        )

    return text


# ==========================================
# 4. EXTRACT SKILLS
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

    return found_skills


# ==========================================
# 5. CALCULATE RESUME SCORE
# ==========================================

def calculate_score(resume_text):

    found = extract_skills(resume_text)

    score = round(
        len(found) * 100 / len(KNOWN_SKILLS)
    )

    return max(0, min(100, score))


# ==========================================
# 6. MATCH JOBS
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
# 7. SKILL ANALYSIS
# ==========================================

def skill_analysis(resume_text):

    found = extract_skills(resume_text)

    missing = [
        skill for skill in KNOWN_SKILLS
        if skill not in found
    ]

    if len(found) >= 10:

        level = "Excellent"

        message = (
            "Your resume contains a wide range of "
            "predefined skills."
        )

    elif len(found) >= 6:

        level = "Good"

        message = (
            "Your resume contains several relevant skills."
        )

    elif len(found) >= 3:

        level = "Intermediate"

        message = (
            "Your resume has some relevant skills. "
            "Consider developing additional skills."
        )

    else:

        level = "Needs Improvement"

        message = (
            "Your resume contains few predefined skills. "
            "Consider adding relevant skills you actually possess."
        )

    suggestions = []

    if "python" not in found:
        suggestions.append(
            "Consider learning Python programming."
        )

    if "sql" not in found:
        suggestions.append(
            "Learn SQL for database management."
        )

    if "git" not in found and "github" not in found:
        suggestions.append(
            "Learn Git and GitHub for project management."
        )

    if "machine learning" not in found:
        suggestions.append(
            "Explore machine learning fundamentals."
        )

    if "communication" not in found:
        suggestions.append(
            "Include relevant communication experience if applicable."
        )

    if not suggestions:
        suggestions.append(
            "Continue improving your skills through practical projects."
        )

    return {
        "found": found,
        "missing": missing,
        "level": level,
        "message": message,
        "suggestions": suggestions
    }


# ==========================================
# 8. EXPERIENCE ESTIMATION
# ==========================================

def extract_experience(resume_text):

    text = resume_text.lower()

    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
        text
    )

    if matches:

        return max(
            float(value) for value in matches
        )

    return 0


# ==========================================
# 9. GENERATE FULL REPORT
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
        "Skills Found: " + ", ".join(skills["found"])
    )

    report.append(
        "Skills Not Found: " + ", ".join(skills["missing"])
    )

    report.append("\nEXPERIENCE ESTIMATION")

    report.append(
        str(experience) + " years (estimated from resume text)"
    )

    report.append("\nJOB MATCHING")

    for job in jobs:

        report.append("\n" + job["title"])

        report.append(
            "Match: " + str(job["match"]) + "%"
        )

        report.append(
            "Matched Skills: " + ", ".join(job["matched"])
        )

        report.append(
            "Missing Skills: " + ", ".join(job["missing"])
        )

    report.append("\nIMPROVEMENT SUGGESTIONS")

    for suggestion in skills["suggestions"]:
        report.append("- " + suggestion)

    report.append("\n" + "=" * 45)

    report.append(
        "Note: This is rule-based analysis using sample job profiles."
    )

    return "\n".join(report)
