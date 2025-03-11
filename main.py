from agents.agent1_keyword_extraction import KeywordExtractionAgent
from agents.agent2_summarization import SummarizationAgent
from agents.agent3_similarity import SimilarityAgent

def main():
    resume_file = "data/resumes/KATHAN_JOSHI_RESUME.pdf"
    job_description_file = "data\job_descriptions\ds.txt"

    candidate_email = "joshikathan03@gmail.com"

    agent1 = KeywordExtractionAgent()
    agent2 = SummarizationAgent()
    agent3 = SimilarityAgent()

    print("Processing resume...")
    entities = agent1.process_resume(resume_file)
    print("Extracted Entities:", entities)

    summary = agent2.process_resume(resume_file)
    print("Summary:", summary)

    # score = agent3.process_resume(resume_file, job_description_file, entities.get("email"))
    score = agent3.process_resume(resume_file, job_description_file, candidate_email)
    print("Similarity Score:", score)

if __name__ == "__main__":
    main()