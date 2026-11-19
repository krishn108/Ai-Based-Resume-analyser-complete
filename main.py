
import streamlit as st

from backend import (
    read_resume,
    calculate_score,
    find_matching_jobs,
    skill_analysis,
    generate_report
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Based Resume Analyser",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "resume_text": "",
    "resume_filename": "",
    "resume_score": None,
    "matching_jobs": None,
    "skills": None,
    "report": None,
    "upload_key": 0,
    "uploaded": False
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("📄 Resume Analyser")

    st.write("Your career analysis assistant.")

    st.divider()

    st.subheader("Navigation")

    st.info(
        "Upload your resume and use the analysis "
        "tools to explore your skills and job matches."
    )

    st.divider()

    st.subheader("Supported Formats")

    st.write("📕 PDF")
    st.write("📘 DOCX")

    st.divider()

    st.caption("Developed using Python and Streamlit.")


# ==========================================
# MAIN HEADER
# ==========================================

st.title("📄 AI Based Resume Analyser")

st.subheader(
    "Understand your resume. Discover your potential."
)

st.write(
    "Analyse your technical skills, calculate skill coverage, "
    "discover suitable job opportunities and identify areas "
    "for improvement."
)

st.divider()


# ==========================================
# DASHBOARD METRICS
# ==========================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Resume Status",
    "Uploaded" if st.session_state.resume_text else "Not Uploaded"
)

col2.metric(
    "Resume Score",
    str(st.session_state.resume_score) + "%"
    if st.session_state.resume_score is not None
    else "Not Calculated"
)

col3.metric(
    "Job Recommendations",
    len(st.session_state.matching_jobs)
    if st.session_state.matching_jobs is not None
    else 0
)

st.divider()


# ==========================================
# UPLOAD RESUME
# ==========================================

st.header("1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Select your resume in PDF or DOCX format",
    type=["pdf", "docx"],
    key="resume_upload_" + str(st.session_state.upload_key)
)

if uploaded_file is not None:

    st.success(
        "Selected File: " + uploaded_file.name
    )


# ==========================================
# TOOL BUTTONS
# ==========================================

st.header("2. Resume Analysis Tools")

col1, col2 = st.columns(2)

# ------------------------------------------
# BUTTON 1: UPLOAD RESUME
# ------------------------------------------

with col1:

    if st.button(
        "📂 Upload Resume",
        use_container_width=True
    ):

        if uploaded_file is None:

            st.warning("Please select a resume first.")

        else:

            st.session_state.resume_filename = uploaded_file.name
            st.session_state.resume_text = ""
            st.session_state.resume_score = None
            st.session_state.matching_jobs = None
            st.session_state.skills = None
            st.session_state.report = None
            st.session_state.uploaded = True

            st.success(
                "Resume selected successfully. Now click Read Resume File."
            )


# ------------------------------------------
# BUTTON 2: READ RESUME FILE
# ------------------------------------------

with col2:

    if st.button(
        "📖 Read Resume File",
        use_container_width=True
    ):

        if uploaded_file is None:

            st.warning("Please select a resume first.")

        else:

            try:

                with st.spinner("Reading your resume..."):

                    extracted_text = read_resume(uploaded_file)

                st.session_state.resume_text = extracted_text
                st.session_state.resume_filename = uploaded_file.name
                st.session_state.resume_score = None
                st.session_state.matching_jobs = None
                st.session_state.skills = None
                st.session_state.report = None
                st.session_state.uploaded = True

                st.success(
                    "Resume successfully read and processed!"
                )

            except Exception as error:

                st.error(str(error))


# ------------------------------------------
# BUTTON 3: RESUME SCORE
# ------------------------------------------

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "📊 Calculate Resume Score",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Please read your resume first.")

        else:

            st.session_state.resume_score = calculate_score(
                st.session_state.resume_text
            )

            st.success("Resume score calculated successfully!")


# ------------------------------------------
# BUTTON 4: FIND MATCHING JOBS
# ------------------------------------------

with col2:

    if st.button(
        "🎯 Find Matching Jobs",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Please read your resume first.")

        else:

            st.session_state.matching_jobs = find_matching_jobs(
                st.session_state.resume_text
            )

            st.success("Job matching completed!")


# ------------------------------------------
# BUTTON 5: SKILL ANALYSIS
# ------------------------------------------

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🧠 Skill Analysis",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Please read your resume first.")

        else:

            st.session_state.skills = skill_analysis(
                st.session_state.resume_text
            )

            st.success("Skill analysis completed!")


# ------------------------------------------
# BUTTON 6: FULL ANALYSIS REPORT
# ------------------------------------------

with col2:

    if st.button(
        "📑 View Full Analysis Report",
        use_container_width=True
    ):

        if not st.session_state.resume_text:

            st.warning("Please read your resume first.")

        else:

            st.session_state.report = generate_report(
                st.session_state.resume_text,
                st.session_state.resume_filename
            )

            st.success("Full report generated!")


# ------------------------------------------
# BUTTON 7: CLEAR / RESET
# ------------------------------------------

if st.button(
    "🔄 Clear / Reset Everything",
    use_container_width=True
):

    next_upload_key = st.session_state.upload_key + 1

    st.session_state.clear()

    st.session_state.upload_key = next_upload_key

    st.rerun()


st.divider()


# ==========================================
# RESUME RESULTS
# ==========================================

st.header("3. Resume Results")


# ------------------------------------------
# EXTRACTED RESUME
# ------------------------------------------

if st.session_state.resume_text:

    with st.expander(
        "📄 View Extracted Resume Text",
        expanded=False
    ):

        st.caption(
            "File: " + st.session_state.resume_filename
        )

        st.text_area(
            "Extracted Information",
            value=st.session_state.resume_text,
            height=250,
            disabled=True
        )


# ------------------------------------------
# RESUME SCORE DISPLAY
# ------------------------------------------

if st.session_state.resume_score is not None:

    st.subheader("⭐ Resume Skill Coverage Score")

    score = st.session_state.resume_score

    st.progress(score)

    col1, col2 = st.columns(2)

    col1.metric(
        "Skill Coverage",
        str(score) + "%"
    )

    if score >= 70:

        col2.success("Good skill coverage")

    elif score >= 40:

        col2.info("Moderate skill coverage")

    else:

        col2.warning("More relevant skills may be needed")

    st.caption(
        "The score measures the percentage of predefined "
        "job-related skills found in your resume. It is not "
        "an overall resume quality or hiring score."
    )


# ------------------------------------------
# SKILL ANALYSIS DISPLAY
# ------------------------------------------

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

        st.markdown("#### ✅ Skills Found")

        if skills["found"]:

            for skill in skills["found"]:
                st.write("🟢 " + skill.title())

        else:

            st.write("No predefined skills detected.")

    with col2:

        st.markdown("#### 📌 Skills Not Found")

        if skills["missing"]:

            for skill in skills["missing"]:
                st.write("⚪ " + skill.title())

        else:

            st.write("All predefined skills detected.")

    st.markdown("#### 💡 Improvement Suggestions")

    for suggestion in skills["suggestions"]:

        st.write("• " + suggestion)


# ------------------------------------------
# JOB MATCHING DISPLAY
# ------------------------------------------

if st.session_state.matching_jobs is not None:

    st.divider()

    st.subheader("🎯 Matching Job Opportunities")

    st.write(
        "These recommendations are ranked according "
        "to the skills found in your resume."
    )

    for index, job in enumerate(
        st.session_state.matching_jobs,
        start=1
    ):

        with st.container(border=True):

            st.markdown(
                "### " + str(index) + ". " + job["title"]
            )

            st.write(job["description"])

            st.metric(
                "Job Match Percentage",
                str(job["match"]) + "%"
            )

            st.progress(job["match"])

            st.markdown("**Matched Skills**")

            if job["matched"]:

                st.success(
                    ", ".join(job["matched"])
                )

            else:

                st.write("No matching skills detected.")

            st.markdown("**Missing Skills**")

            if job["missing"]:

                st.warning(
                    ", ".join(job["missing"])
                )

            else:

                st.success("All required skills detected!")


# ------------------------------------------
# FULL REPORT DISPLAY
# ------------------------------------------

if st.session_state.report is not None:

    st.divider()

    st.subheader("📑 Complete Resume Analysis Report")

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
# FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Based Resume Analyser | "
    "Developed using Python | "
    "Resume Parsing • Skill Analysis • Job Matching"
)

st.caption(
    "Disclaimer: This application provides basic "
    "rule-based resume analysis and sample job recommendations. "
    "It does not guarantee employment."
)
