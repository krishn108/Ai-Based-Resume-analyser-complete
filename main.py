
import streamlit as st

from backend import (
    read_resume,
    calculate_score,
    find_matching_jobs,
    skill_analysis,
    generate_report
)


# ==========================================
# 1. PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Based Resume Analyser",
    page_icon="📄",
    layout="wide"
)


# ==========================================
# 2. SESSION STATE
# ==========================================

defaults = {

    "resume_text": "",

    "resume_filename": "",

    "resume_uploaded": False,

    "resume_score": None,

    "matching_jobs": None,

    "skills": None,

    "report": None

}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================
# 3. RESET FUNCTION
# ==========================================

def clear_application():

    for key in list(st.session_state.keys()):

        del st.session_state[key]

    st.rerun()


# ==========================================
# 4. SIDEBAR
# ==========================================

with st.sidebar:

    st.title("📄 AI Resume Analyser")

    st.write("Your Career Analysis Assistant")

    st.divider()

    st.subheader("Project Modules")

    st.write("🏠 Dashboard")

    st.write("📤 Resume Upload")

    st.write("📖 Resume Reading")

    st.write("📊 Resume Score")

    st.write("🧠 Skill Analysis")

    st.write("🎯 Job Matching")

    st.write("📑 Full Report")

    st.divider()

    st.subheader("Supported Files")

    st.write("📕 PDF")

    st.write("📘 DOCX")

    st.divider()

    st.caption("Developed using Python and Streamlit")


# ==========================================
# 5. MAIN HEADER
# ==========================================

st.title("📄 AI Based Resume Analyser")

st.subheader(
    "Discover Your Skills. Improve Your Resume."
)

st.write(
    "Upload your resume to analyse technical skills, "
    "calculate skill coverage, identify missing skills "
    "and discover suitable career opportunities."
)

st.divider()


# ==========================================
# 6. DASHBOARD
# ==========================================

st.header("📊 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:

    status = (
        "Uploaded"
        if st.session_state.resume_text
        else "Not Uploaded"
    )

    st.metric("Resume Status", status)

with col2:

    score = st.session_state.resume_score

    st.metric(
        "Resume Score",
        str(score) + "%"
        if score is not None
        else "Not Calculated"
    )

with col3:

    jobs = st.session_state.matching_jobs

    st.metric(
        "Matching Jobs",
        len(jobs) if jobs is not None else 0
    )

st.divider()


# ==========================================
# 7. UPLOAD RESUME
# ==========================================

st.header("📤 1. Upload Your Resume")

st.info(
    "Choose a PDF or DOCX file from your phone's "
    "Internal Storage or computer. Maximum size: 10 MB."
)

# IMPORTANT:
# This is the simple uploader that passed your test.
# No Google Drive API and no dynamic widget key.

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    accept_multiple_files=False
)

if uploaded_file is not None:

    st.success(
        "Selected File: " + uploaded_file.name
    )

    st.write(
        "File Size: "
        + str(round(uploaded_file.size / 1024, 2))
        + " KB"
    )


# ==========================================
# 8. BUTTON 1 - UPLOAD RESUME
# ==========================================

if st.button(
    "📂 Upload Resume",
    use_container_width=True
):

    if uploaded_file is None:

        st.warning("Please select a resume first.")

    else:

        st.session_state.resume_uploaded = True

        st.session_state.resume_filename = uploaded_file.name

        st.session_state.resume_text = ""

        st.session_state.resume_score = None

        st.session_state.matching_jobs = None

        st.session_state.skills = None

        st.session_state.report = None

        st.success(
            "Resume selected successfully! "
            "Now click Read Resume File."
        )


# ==========================================
# 9. BUTTON 2 - READ RESUME
# ==========================================

if st.button(
    "📖 Read Resume File",
    use_container_width=True
):

    if uploaded_file is None:

        st.warning("Please select a resume first.")

    else:

        try:

            with st.spinner("Reading your resume..."):

                text = read_resume(uploaded_file)

            st.session_state.resume_text = text

            st.session_state.resume_filename = uploaded_file.name

            st.session_state.resume_uploaded = True

            st.session_state.resume_score = None

            st.session_state.matching_jobs = None

            st.session_state.skills = None

            st.session_state.report = None

            st.success(
                "Resume text extracted successfully!"
            )

        except Exception as error:

            st.error(
                "Resume reading failed: " + str(error)
            )


st.divider()


# ==========================================
# 10. RESUME ANALYSIS TOOLS
# ==========================================

st.header("🛠️ 2. Resume Analysis Tools")

col1, col2 = st.columns(2)


# BUTTON 3 - RESUME SCORE

with col1:

    if st.button(
        "📊 Resume Score",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Read your resume first.")

        else:

            st.session_state.resume_score = calculate_score(
                st.session_state.resume_text
            )

            st.success("Resume score calculated!")


# BUTTON 4 - JOB MATCHING

with col2:

    if st.button(
        "🎯 Find Matching Jobs",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Read your resume first.")

        else:

            st.session_state.matching_jobs = find_matching_jobs(
                st.session_state.resume_text
            )

            st.success("Job matching completed!")


col1, col2 = st.columns(2)


# BUTTON 5 - SKILL ANALYSIS

with col1:

    if st.button(
        "🧠 Skill Analysis",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Read your resume first.")

        else:

            st.session_state.skills = skill_analysis(
                st.session_state.resume_text
            )

            st.success("Skill analysis completed!")


# BUTTON 6 - FULL REPORT

with col2:

    if st.button(
        "📑 View Full Analysis Report",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Read your resume first.")

        else:

            st.session_state.report = generate_report(
                st.session_state.resume_text,
                st.session_state.resume_filename
            )

            st.success("Full report generated!")


# BUTTON 7 - RESET

if st.button(
    "🔄 Clear / Reset Everything",
    use_container_width=True
):

    clear_application()


st.divider()


# ==========================================
# 11. EXTRACTED RESUME
# ==========================================

st.header("📋 3. Resume Results")

if st.session_state.resume_text:

    st.subheader("📄 Extracted Resume Text")

    st.caption(
        "File: " + st.session_state.resume_filename
    )

    with st.expander("View Resume Content"):

        st.text_area(
            "Resume Information",
            value=st.session_state.resume_text,
            height=250,
            disabled=True
        )


# ==========================================
# 12. RESUME SCORE
# ==========================================

if st.session_state.resume_score is not None:

    st.divider()

    st.subheader("⭐ Resume Skill Coverage Score")

    score = st.session_state.resume_score

    st.progress(score)

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Skill Coverage",
            str(score) + "%"
        )

    with col2:

        if score >= 70:

            st.success("Good Skill Coverage")

        elif score >= 40:

            st.info("Moderate Skill Coverage")

        else:

            st.warning("Needs Improvement")

    st.caption(
        "This score measures the percentage of predefined "
        "job-related skills found in the resume. "
        "It is not an overall resume quality score."
    )


# ==========================================
# 13. SKILL ANALYSIS
# ==========================================

if st.session_state.skills is not None:

    skills = st.session_state.skills

    st.divider()

    st.subheader("🧠 Detailed Skill Analysis")

    st.write(
        "**Skill Level:** " + skills["level"]
    )

    st.info(skills["message"])

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ✅ Skills Found")

        if skills["found"]:

            for skill in skills["found"]:

                st.write("🟢 " + skill.title())

        else:

            st.write("No predefined skills detected.")

    with col2:

        st.markdown("### 📌 Skills Not Found")

        for skill in skills["missing"]:

            st.write("⚪ " + skill.title())

    st.markdown("### 💡 Improvement Suggestions")

    for suggestion in skills["suggestions"]:

        st.write("• " + suggestion)


# ==========================================
# 14. JOB MATCHING RESULTS
# ==========================================

if st.session_state.matching_jobs is not None:

    st.divider()

    st.subheader("🎯 Matching Job Recommendations")

    for index, job in enumerate(
        st.session_state.matching_jobs,
        start=1
    ):

        with st.container(border=True):

            st.markdown(
                "### "
                + str(index)
                + ". "
                + job["title"]
            )

            st.write(job["description"])

            st.metric(
                "Job Match",
                str(job["match"]) + "%"
            )

            st.progress(job["match"])

            st.markdown("**Matched Skills**")

            if job["matched"]:

                st.success(
                    ", ".join(job["matched"])
                )

            else:

                st.write("No matching skills found.")

            st.markdown("**Missing Skills**")

            if job["missing"]:

                st.warning(
                    ", ".join(job["missing"])
                )

            else:

                st.success(
                    "All required skills detected!"
                )


# ==========================================
# 15. FULL REPORT
# ==========================================

if st.session_state.report is not None:

    st.divider()

    st.subheader("📑 Full Resume Analysis Report")

    st.text_area(
        "Generated Report",
        value=st.session_state.report,
        height=400,
        disabled=True
    )

    st.download_button(
        label="⬇️ Download Full Analysis Report",
        data=st.session_state.report,
        file_name="Resume_Analysis_Report.txt",
        mime="text/plain",
        use_container_width=True
    )


# ==========================================
# 16. FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Based Resume Analyser | Python Project"
)

st.caption(
    "Resume Parsing | Resume Scoring | Skill Analysis | Job Matching"
)

st.caption(
    "This application uses predefined skills and sample job "
    "profiles. Results are informational and do not guarantee employment."
            )
