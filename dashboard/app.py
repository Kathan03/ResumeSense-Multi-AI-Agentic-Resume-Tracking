import sys
from pathlib import Path

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from agents.agent4_chatbot_agent import ChatbotAgent
from agents.agent1_keyword_extraction import KeywordExtractionAgent
from agents.agent2_summarization import SummarizationAgent
from agents.agent3_similarity import SimilarityAgent

st.title("Resume Ranking System")

# File uploads
resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
job_description_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf", "docx"])

if resume_file and job_description_file:
    # Save uploaded files
    resume_name = resume_file.name
    resume_path = f"data/resumes/{resume_name}"
    job_description_path = f"data/job_descriptions/{job_description_file.name}"
    with open(resume_path, "wb") as f:
        f.write(resume_file.getbuffer())
    with open(job_description_path, "wb") as f:
        f.write(job_description_file.getbuffer())

    # Initialize agents
    agent1 = KeywordExtractionAgent()
    agent2 = SummarizationAgent()
    agent3 = SimilarityAgent()
    chatbot_agent = ChatbotAgent(resume_path, job_description_path)

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

    # Chatbot Interaction
    st.subheader("Chat with Resume")
    query = st.text_input("Ask a question about the resume or job description")
    if st.button("Submit Query"):
        if query:
            answer = chatbot_agent.answer_query(query)
            st.write("Answer:", answer)