import streamlit as st
import PyPDF2
import re


# -------------------------------
# Page Setup
# -------------------------------

st.set_page_config(
    page_title="TalentLens AI",
    page_icon="🤖",
    layout="wide"
)


# -------------------------------
# CSS
# -------------------------------

st.markdown(
    """
    <style>

    body {
        background-color: #f5f6fa;
    }

    .block-container {
        padding-top: 1.5rem;
    }

    .header {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
    }

    .header h1 {
        margin: 0;
        font-size: 35px;
    }

    .header p {
        margin: 8px 0 0;
        font-size: 16px;
    }

    .card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e2e4ec;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }

    .candidate-name {
        font-size: 19px;
        font-weight: bold;
    }

    .score {
        font-size: 32px;
        font-weight: bold;
        color: #4f46e5;
    }

    .skill {
        display: inline-block;
        background: #e8f7ee;
        color: #137a48;
        padding: 6px 10px;
        border-radius: 15px;
        margin: 3px;
        font-size: 13px;
    }

    .missing {
        display: inline-block;
        background: #fff0f0;
        color: #c62828;
        padding: 6px 10px;
        border-radius: 15px;
        margin: 3px;
        font-size: 13px;
    }

    .recommendation {
        background: #f0f4ff;
        color: #273c75;
        padding: 12px;
        border-radius: 10px;
        margin-top: 12px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div class="header">
        <h1>🤖 TalentLens AI</h1>
        <p>Smart Resume Analysis • Skill Matching • Candidate Shortlisting</p>
    </div>
    """,
    unsafe_allow_html=True
)
skills = [
    "Python", "SQL", "Pandas","NumPy", "Machine Learning", "Deep Learning", "Streamlit", "React",
    "Java","C++", "JavaScript", "HTML", "CSS", "Git", "GitHub", "Node.js", "MongoDB", "Power BI",
    "Tableau", "Excel", "TensorFlow", "PyTorch", "NLP", "Data Analysis"
]

skill_aliases = {
    "Pandas": ["pandas", "panda s"],
    "NumPy": ["numpy", "num py", "num-py", "num_py"],
    "Machine Learning": ["machine learning", "machine-learning"],
    "Deep Learning": ["deep learning", "deep-learning"],
    "Node.js": ["node.js", "nodejs", "node js"],
    "Power BI": ["power bi", "powerbi"],
    "Data Analysis": ["data analysis", "data-analysis"],
    "C++": ["c++"],
    "JavaScript": ["javascript", "java script"],
    "GitHub": ["github", "git hub"]
}
def extract_pdf_text(uploaded_file):
    """
    Extract text from PDF.
    """
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text
def normalize_text(text):
    """
    Convert text to lowercase and normalize spaces.
    """
    text = text.lower()
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()
def compact_text(text):
    """
    Remove spaces and special characters.
    Example:
    Num Py -> numpy
    Num-py -> numpy
    """
    return re.sub(
        r"[^a-z0-9+#]",
        "",
        text.lower()
    )
def find_skills(text):
    """
    Find skills from JD or resume text.
    """
    normalized_text = normalize_text(text)
    compact_resume_text = compact_text(normalized_text)

    found_skills = []
    for skill in skills:

        aliases = skill_aliases.get(
            skill,
            [skill]
        )

        skill_found = False

        for alias in aliases:
            alias = normalize_text(alias)
            pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"
            if re.search(pattern, normalized_text):
                skill_found = True
                break
            compact_alias = compact_text(alias)

            if compact_alias and compact_alias in compact_resume_text:
                skill_found = True
                break
        if skill_found:
            found_skills.append(skill)

    return found_skills

def get_recommendation(match_percentage, missing_skills):

    if match_percentage >= 80:

        return (
            "Highly recommended. Candidate has most of the required "
            "skills and can be shortlisted for the next interview round."
        )

    elif match_percentage >= 60:
        if missing_skills:

            missing = ", ".join(missing_skills)
            return (
                "Recommended for further evaluation. Candidate has a "
                "good skill match but should improve knowledge of: "
                f"{missing}."
            )
        return (
            "Recommended for the next round. Candidate satisfies "
            "most of the required skills."
        )

    else:
        if missing_skills:

            missing = ", ".join(missing_skills)

            return (
                "Not recommended currently. Candidate is missing "
                f"important skills such as: {missing}."
            )

        return (
            "Not recommended currently. Candidate has a low match score."
        )
left_col, right_col = st.columns(
    [1, 1],
    gap="large"
)
with left_col:

   
    st.markdown("### 📄 Upload Resumes")

    resumes = st.file_uploader(
        "Upload PDF resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    if resumes:

        st.success(
            f"{len(resumes)} resume(s) uploaded"
        )

        for resume in resumes:

            st.write(
                f"📄 {resume.name}"
            )

    st.markdown("### 📋 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=230,
        placeholder=(
            "Example: Python Developer with SQL, Pandas "
            "and Machine Learning..."
        )
    )

    screen_button = st.button(
        "🚀 Start Resume Screening",
        use_container_width=True
    )

if screen_button:

    if not job_description.strip():

        st.warning(
            "Please enter a Job Description."
        )

    elif not resumes:

        st.warning(
            "Please upload at least one resume."
        )

    else:

        required_skills = find_skills(
            job_description
        )

        if not required_skills:

            st.warning(
                "No known skills found in the Job Description."
            )

        else:

            results = []

            for resume_file in resumes:

                resume_text = extract_pdf_text(
                    resume_file
                )

                resume_skills = find_skills(
                    resume_text
                )

                matched_skills = []
                unmatched_skills = []

                for skill in required_skills:

                    if skill in resume_skills:

                        matched_skills.append(skill)

                    else:

                        unmatched_skills.append(skill)

                total_skills = len(required_skills)
                matched_count = len(matched_skills)

                match_percentage = (
                    matched_count / total_skills
                ) * 100

                if match_percentage >= 60:

                    status = "Shortlisted"

                else:

                    status = "Rejected"

                recommendation = get_recommendation(
                    match_percentage,
                    unmatched_skills
                )

                results.append(
                    {
                        "name": resume_file.name,
                        "match": match_percentage,
                        "matched": matched_skills,
                        "missing": unmatched_skills,
                        "status": status,
                        "recommendation": recommendation
                    }
                )

            results.sort(
                key=lambda x: x["match"],
                reverse=True
            )

            st.session_state["results"] = results
            st.session_state["required_skills"] = required_skills

            st.success(
                "Resume screening completed successfully."
            )


# -------------------------------
# Display Stored Results
# -------------------------------

if "results" in st.session_state:

    results = st.session_state["results"]
    required_skills = st.session_state["required_skills"]

else:

    results = []
    required_skills = []

# -------------------------------
# Resume Statistics
# -------------------------------

total_resumes = len(results)

shortlisted_count = sum(
    1
    for candidate in results
    if candidate["status"] == "Shortlisted"
)

rejected_count = sum(
    1
    for candidate in results
    if candidate["status"] == "Rejected"
)

st.markdown("### 📊 Resume Screening Summary")

stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:

    st.markdown(
        f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:30px;">📄</div>
            <div style="font-size:14px; color:#666;">
                Total Resumes
            </div>
            <div style="font-size:32px; font-weight:bold; color:#4f46e5;">
                {total_resumes}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with stat_col2:

    st.markdown(
        f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:30px;">⭐</div>
            <div style="font-size:14px; color:#666;">
                Shortlisted Candidates
            </div>
            <div style="font-size:32px; font-weight:bold; color:#137a48;">
                {shortlisted_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with stat_col3:

    st.markdown(
        f"""
        <div class="card" style="text-align:center;">
            <div style="font-size:30px;">❌</div>
            <div style="font-size:14px; color:#666;">
                Rejected Candidates
            </div>
            <div style="font-size:32px; font-weight:bold; color:#c62828;">
                {rejected_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# -------------------------------
# Right Section: Candidate View
# -------------------------------

with right_col:

    st.subheader("👤 Candidate Analysis View")

    if results:

        candidate_names = [
            candidate["name"]
            for candidate in results
        ]

        selected_name = st.selectbox(
            "Select Candidate",
            candidate_names
        )

        selected_candidate = next(
            candidate
            for candidate in results
            if candidate["name"] == selected_name
        )

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="candidate-name">
                📄 {selected_candidate["name"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="score">
                {selected_candidate["match"]:.0f}%
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            int(selected_candidate["match"])
        )

        if selected_candidate["status"] == "Shortlisted":

            st.success("⭐ Recommended")

        else:

            st.error("❌ Rejected")

        st.markdown(
            f"""
            <div class="recommendation">
                <b>💡 Recommendation:</b><br>
                {selected_candidate["recommendation"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    else:

        st.info(
            "Candidate details will appear here."
        )


# -------------------------------
# Horizontal Candidate Skill Analysis
# -------------------------------

if results:

    st.divider()

    st.subheader(
        "📋 Detailed Candidate Skill Analysis"
    )

    candidate_columns = st.columns(
        len(results),
        gap="medium"
    )

    for index, candidate in enumerate(results):

        with candidate_columns[index]:

            with st.container(border=True):

                # Candidate Name

                st.markdown(
                    f"### 📄 {candidate['name']}"
                )

                # Match Percentage

                st.markdown(
                    f"**🎯 Match Score: {candidate['match']:.0f}%**"
                )

                st.progress(
                    int(candidate["match"])
                )

                # Status

                if candidate["status"] == "Shortlisted":

                    st.success("⭐ Shortlisted")

                else:

                    st.error("❌ Rejected")


                # Recommendation

                st.markdown(
                    f"""
                    <div class="recommendation">
                        <b>💡 Recommendation</b><br>
                        {candidate["recommendation"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # Skill Counts

                st.markdown(
                    f"""
                    **📋 Required Skills:** {len(required_skills)}  
                    **🟢 Matching Skills:** {len(candidate["matched"])}  
                    **🔴 Missing Skills:** {len(candidate["missing"])}
                    """
                )


                # Required Skills

                st.markdown(
                    "**📋 Required Skills**"
                )

                for skill in required_skills:

                    st.markdown(
                        f'<span class="skill">🔹 {skill}</span>',
                        unsafe_allow_html=True
                    )


                # Matching Skills

                st.markdown(
                    "**🟢 Matching Skills**"
                )

                if candidate["matched"]:

                    for skill in candidate["matched"]:

                        st.markdown(
                            f'<span class="skill">✓ {skill}</span>',
                            unsafe_allow_html=True
                        )

                else:

                    st.write(
                        "No matching skills found."
                    )


                # Unmatched Skills

                st.markdown(
                    "**🔴 Unmatched Skills**"
                )

                if candidate["missing"]:

                    for skill in candidate["missing"]:

                        st.markdown(
                            f'<span class="missing">✗ {skill}</span>',
                            unsafe_allow_html=True
                        )

                else:

                    st.success(
                        "All required skills matched!"
                    )


# -------------------------------
# Footer
# -------------------------------

st.divider()

st.caption(
    "TalentLens AI | AI Resume Screening System"
)