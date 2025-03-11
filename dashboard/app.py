import streamlit as st
from agents.agent1_keyword_extraction import KeywordExtractionAgent
from agents.agent2_summarization import SummarizationAgent
from agents.agent3_similarity import SimilarityAgent

st.title("Resume Ranking System")

# File upload for resume
resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
job_description_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf", "docx"])

if resume_file and job_description_file:
    # Save uploaded files temporarily
    resume_path = f"data/resumes/{resume_file.name}"
    job_description_path = f"data/job_descriptions/{job_description_file.name}"
    with open(resume_path, "wb") as f:
        f.write(resume_file.getbuffer())
    with open(job_description_path, "wb") as f:
        f.write(job_description_file.getbuffer())

    # Initialize agents
    agent1 = KeywordExtractionAgent()
    agent2 = SummarizationAgent()
    agent3 = SimilarityAgent()

    # Agent 1: Keyword Extraction
    st.subheader("Extracted Keywords")
    entities = agent1.process_resume(resume_path)
    if entities:
        st.write(entities)

    # Agent 2: Summarization
    st.subheader("Resume Summary")
    summary = agent2.process_resume(resume_path)
    if summary:
        st.write(summary)

    # Agent 3: Similarity Scoring
    st.subheader("Similarity Score")
    score = agent3.process_resume(resume_path, job_description_path, entities.get("email"))
    if score:
        st.write(f"Similarity Score: {score:.2f}")