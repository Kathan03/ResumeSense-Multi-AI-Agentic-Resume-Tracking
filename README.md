# Multi-Agent Resume Parsing & Candidate Ranking System

## Overview
This project builds a system to ingest resumes, extract keywords, generate summaries, and rank candidates based on their alignment with job descriptions. It includes a Streamlit dashboard for recruiters and supports automated email notifications.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Install spaCy model: `python -m spacy download en_core_web_sm`
4. Run the dashboard: `streamlit run dashboard/app.py`

## Usage
- Upload resumes to the `data/resumes/` directory.
- Add job descriptions to the `data/job_descriptions/` directory.
- Use the Streamlit dashboard to process resumes and view rankings.