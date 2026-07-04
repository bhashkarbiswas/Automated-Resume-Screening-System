import streamlit as st
import time
import os
import csv
from datetime import datetime

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from matcher import calculate_match_score

st.set_page_config(
    page_title="Automated Resume Screening System",
    layout="wide"
)

EVAL_FOLDER = "evaluation"
RESULTS_FILE = os.path.join(EVAL_FOLDER, "results.csv")

os.makedirs(EVAL_FOLDER, exist_ok=True)

if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Date",
            "Resume",
            "Actual_Label",
            "Predicted_Label",
            "Match_Score",
            "Matched_Skills",
            "Missing_Skills",
            "Processing_Time"
        ])

st.markdown(
    """
    <div style="
        background: linear-gradient(
            135deg,
            #00d4aa 0%,
            #2563eb 25%,
            #4f46e5 50%,
            #7c3aed 75%,
            #d946ef 100%
        );
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    ">
        <h1 style="
            color: white;
            margin: 0;
            font-size: 42px;
            font-weight: 700;
        ">
            Automated Resume Screening System
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center; font-size:18px; color:gray;'>
    AI-Powered Resume Screening, Evaluation & Job Recommendation System
    </p>
    """,
    unsafe_allow_html=True
)

mode = st.sidebar.radio(
    "Select Mode",
    ["Recruiter Mode", "Job Seeker Mode"]
)

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if st.button("Analyze Resume"):

    if uploaded_resume is None:
        st.error("Please upload a resume.")

    elif job_description.strip() == "":
        st.error("Please enter a job description.")

    else:

        start_time = time.perf_counter()

        resume_text = extract_text_from_pdf(uploaded_resume)

        if not resume_text:
            st.error("Unable to extract text from the uploaded PDF.")
            st.stop()

        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(job_description)

        score, matched, missing = calculate_match_score(
            resume_skills,
            jd_skills
        )

        processing_time = round(
            time.perf_counter() - start_time,
            3
        )

        if score >= 80:
            verdict = "Highly Suitable Candidate"
        elif score >= 60:
            verdict = "Suitable Candidate"
        elif score >= 40:
            verdict = "Moderately Suitable Candidate"
        else:
            verdict = "Not Suitable Candidate"

        with open(
            RESULTS_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            uploaded_resume.name,
            "",                     # Actual Label (fill later)
            verdict,
            round(score, 2),
            ", ".join(matched),
            ", ".join(missing),
            processing_time
        ])

        st.subheader("Analysis Result")

        st.metric(
            "Match Score",
            f"{score:.2f}%"
        )

        st.metric(
            "Processing Time",
            f"{processing_time:.3f} sec"
        )

        st.progress(int(score))

        st.write(f"Total Skills Found: {len(resume_skills)}")
        st.write(f"Matched Skills: {len(matched)}")
        st.write(f"Missing Skills: {len(missing)}")

        st.subheader("Skills Found in Resume")

        if resume_skills:
            for skill in resume_skills:
                st.success(f"✓ {skill}")
        else:
            st.warning("No skills were extracted from the resume.")

        st.subheader("Matched Skills")

        if matched:
            for skill in matched:
                st.success(f"✓ {skill}")
        else:
            st.warning("No matching skills found.")

        st.subheader("Missing Skills")

        if missing:
            for skill in missing:
                st.error(f"✗ {skill}")
        else:
            st.success("No missing skills.")

        st.markdown("---")
        st.subheader("Final Verdict")

        if score >= 80:
            st.success(verdict)

        elif score >= 60:
            st.info(verdict)

        elif score >= 40:
            st.warning(verdict)

        else:
            st.error(verdict)

        if mode == "Job Seeker Mode":

            st.subheader("Recommended Job Roles")

            recommended_jobs = []

            skills_text = " ".join(resume_skills).lower()

            if any(skill in skills_text for skill in [
                "python",
                "machine learning",
                "deep learning",
                "tensorflow",
                "pytorch"
            ]):
                recommended_jobs.extend([
                    "Data Scientist",
                    "Machine Learning Engineer"
                ])

            if any(skill in skills_text for skill in [
                "python",
                "django",
                "flask"
            ]):
                recommended_jobs.append(
                    "Python Developer"
                )

            if any(skill in skills_text for skill in [
                "java",
                "spring boot"
            ]):
                recommended_jobs.append(
                    "Java Developer"
                )

            if any(skill in skills_text for skill in [
                "html",
                "css",
                "javascript",
                "react"
            ]):
                recommended_jobs.append(
                    "Frontend Developer"
                )

            if any(skill in skills_text for skill in [
                "sql",
                "mysql",
                "postgresql",
                "mongodb"
            ]):
                recommended_jobs.append(
                    "Database Developer"
                )

            if any(skill in skills_text for skill in [
                "aws",
                "docker",
                "kubernetes"
            ]):
                recommended_jobs.append(
                    "Cloud Engineer"
                )

            recommended_jobs = sorted(
                list(set(recommended_jobs))
            )

            if recommended_jobs:

                for job in recommended_jobs:
                    st.success(job)

            else:
                st.info(
                    "No suitable job recommendation found."
                )

st.markdown("---")

st.markdown(
    """
    <p style="text-align:center;">
        Developed By:
        <a href="https://github.com/bhashkarbiswas" target="_blank">
            Bhashkar Biswas
        </a>
    </p>
    """,
    unsafe_allow_html=True
)