from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.email_notifications import send_email

class SimilarityAgent:
    def __init__(self, similarity_threshold=0.8):
        self.vectorizer = TfidfVectorizer()
        self.threshold = similarity_threshold

    def calculate_similarity(self, resume_text, job_description_text):
        """Calculate similarity score between resume and job description."""
        documents = [resume_text, job_description_text]
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return similarity_score

    def process_resume(self, resume_file, job_description_file, candidate_email):
        """Process a resume and job description, calculate similarity, and notify if needed."""
        from utils.file_parsing import parse_file
        resume_text = parse_file(resume_file)
        job_description_text = parse_file(job_description_file)
        if resume_text and job_description_text:
            score = self.calculate_similarity(resume_text, job_description_text)
            if score >= self.threshold and candidate_email:
                send_email(candidate_email, "Congratulations!", "You've been shortlisted for the next round.")
            return score
        return None