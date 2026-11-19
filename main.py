
import streamlit as st

from backend import (
    read_resume,
    calculate_score,
    find_matching_jobs,
    skill_analysis,
    generate_report
)


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Based Resume Analyser",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. SESSION DATA
# ==========================================

def initialize_state():

    defaults = {
        "resume_text": "",
        "resume_filename": "",
        "resume_score": None,
        "matching_jobs": None,
        "skills": None,
        "report": None,
        "upload_key": 0
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


initialize_state()


# ==========================================
# 3. RESET FUNCTION
# ==========================================

def reset_application():

    next_key = st.session_state.upload_key + 1

    st.session_state.clear()

    st.session_state.upload_key = next_key


# ==========================================
# 4. SIDEBAR
# ==========================================

with st.sidebar:

    st.title("📄 Resume Analyser")

    st.write("Your career analysis assistant.")

    st.divider()

    st.subheader("Navigation")

    st.write("🏠 Dashboard")
    st.write("📤 Resume Upload")
    st.write("📊 Resume Score")
    st.write("🧠 Skill Analysis")
    st.write("🎯 Job Matching")
    st.write("📑 Analysis Report")

    st.divider()

    st.subheader("Supported Files")

    st.write("📕 PDF")
    st.write("📘 DOCX")

    st.divider()

    st.caption("Powered by Python and Streamlit")


# ==========================================
# 5. MAIN HEADER
# ==========================================

st.title("📄 AI Based Resume Analyser")

st.subheader(
    "Discover your skills. Improve your resume. "
    "Explore career opportunities."
)

st.write(
    "An intelligent resume analysis application "
    "that extracts resume information, identifies "
    "technical skills and recommends suitable jobs."
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
        "Job Recommendations",
        len(jobs) if jobs is not None else 0
    )

st.divider()


# ==========================================
# 7. RESUME UPLOAD
# ==========================================

st.header("📤 1. Upload Your Resume")

st.info(
    "Select a PDF or DOCX resume. "
    "Maximum supported file size: 10 MB."
)

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    accept_multiple_files=False,
    key="resume_upload_" + str(st.session_state.upload_key)
)

if uploaded_file is not None:

    st.success(
        "File selected: " + uploaded_file.name
    )

    st.write(
        "File size: "
        + str(round(uploaded_file.size / 1024, 2))
        + " KB"
    )


# ==========================================
# 8. RESUME PROCESSING
# ==========================================

if st.button(
    "📥 Upload and Read Resume",
    use_container_width=True
):

    if uploaded_file is None:

        st.warning("Please select a PDF or DOCX file first.")

    else:

        try:

            with st.spinner("Processing your resume..."):

                extracted_text = read_resume(uploaded_file)

            st.session_state.resume_text = extracted_text

            st.session_state.resume_filename = uploaded_file.name

            st.session_state.resume_score = None

            st.session_state.matching_jobs = None

            st.session_state.skills = None

            st.session_state.report = None

            st.success(
                "Resume uploaded and processed successfully!"
            )

        except Exception as error:

            st.error(
                "Resume processing failed: " + str(error)
            )


st.divider()


# ==========================================
# 9. RESUME TOOLS
# ==========================================

st.header("🛠️ 2. Resume Analysis Tools")

col1, col2 = st.columns(2)


# RESUME SCORE

with col1:

    if st.button(
        "📊 Resume Score",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Upload and read your resume first.")

        else:

            st.session_state.resume_score = calculate_score(
                st.session_state.resume_text
            )

            st.success("Resume score calculated!")


# JOB MATCHING

with col2:

    if st.button(
        "🎯 Find Matching Jobs",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Upload and read your resume first.")

        else:

            st.session_state.matching_jobs = find_matching_jobs(
                st.session_state.resume_text
            )

            st.success("Job matching completed!")


col1, col2 = st.columns(2)


# SKILL ANALYSIS

with col1:

    if st.button(
        "🧠 Skill Analysis",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Upload and read your resume first.")

        else:

            st.session_state.skills = skill_analysis(
                st.session_state.resume_text
            )

            st.success("Skill analysis completed!")


# FULL REPORT

with col2:

    if st.button(
        "📑 View Full Analysis Report",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Upload and read your resume first.")

        else:

            st.session_state.report = generate_report(
                st.session_state.resume_text,
                st.session_state.resume_filename
            )

            st.success("Full report generated!")


# CLEAR / RESET

if st.button(
    "🔄 Clear / Reset Everything",
    use_container_width=True
):

    reset_application()

    st.rerun()


st.divider()


# ==========================================
# 10. RESULTS SECTION
# ==========================================

st.header("📋 3. Analysis Results")


# ==========================================
# EXTRACTED RESUME
# ==========================================

if st.session_state.resume_text:

    st.subheader("📄 Extracted Resume")

    st.caption(
        "File: " + st.session_state.resume_filename
    )

    with st.expander("View Resume Text", expanded=False):

        st.text_area(
            "Resume Content",
            value=st.session_state.resume_text,
            height=250,
            disabled=True
        )


# ==========================================
# RESUME SCORE
# ==========================================

if st.session_state.resume_score is not None:

    st.subheader("⭐ Resume Skill Coverage")

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

            st.success("Good skill coverage")

        elif score >= 40:

            st.info("Moderate skill coverage")

        else:

            st.warning("More relevant skills may be needed")

    st.caption(
        "This score represents the percentage of predefined "
        "skills detected in the resume. It is not a hiring score."
    )


# ==========================================
# SKILL ANALYSIS
# ==========================================

if st.session_state.skills is not None:

    skills = st.session_state.skills

    st.divider()

    st.subheader("🧠 Detailed Skill Analysis")

    st.write("Skill Level: " + skills["level"])

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
# JOB MATCHING RESULTS
# ==========================================

if st.session_state.matching_jobs is not None:

    st.divider()

    st.subheader("🎯 Job Recommendations")

    st.write(
        "The following jobs are ranked according "
        "to the skills detected in your resume."
    )

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

                st.success(", ".join(job["matched"]))

            else:

                st.write("No matching skills found.")

            st.markdown("**Missing Skills**")

            if job["missing"]:

                st.warning(", ".join(job["missing"]))

            else:

                st.success("All required skills detected!")


# ==========================================
# FULL ANALYSIS REPORT
# ==========================================

if st.session_state.report is not None:

    st.divider()

    st.subheader("📑 Full Analysis Report")

    st.text_area(
        "Report",
        value=st.session_state.report,
        height=400,
        disabled=True
    )

    st.download_button(
        "⬇️ Download Analysis Report",
        data=st.session_state.report,
        file_name="Resume_Analysis_Report.txt",
        mime="text/plain",
        use_container_width=True
    )


# ==========================================
# 11. FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Based Resume Analyser | Developed using Python"
)

st.caption(
    "Resume Parsing | Skill Analysis | Resume Scoring | Job Matching"
)

st.caption(
    "Disclaimer: This application uses predefined skills "
    "and sample job profiles. Its recommendations are "
    "informational and do not guarantee employment."
)
