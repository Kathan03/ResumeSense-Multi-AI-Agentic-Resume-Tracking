import spacy

class KeywordExtractionAgent:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text):
        """Extract entities like skills, experience, education, and email from text."""
        print(text)
        doc = self.nlp(text)
        entities = {
            "skills": [],
            "experience": [],
            "education": [],
            "email": None
        }

        # Simple heuristic for skills (nouns and noun phrases)
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"] and token.text.lower() in ["python", "java", "sql"]:  # Add more skills
                entities["skills"].append(token.text)

        # Extract email using spaCy's entity recognition
        for ent in doc.ents:
            if ent.label_ == "EMAIL":
                entities["email"] = ent.text

        # Placeholder for experience and education (to be expanded)
        return entities

    def process_resume(self, file_path):
        """Process a resume file and return extracted entities."""
        from utils.file_parsing import parse_file
        text = parse_file(file_path)
        if text:
            return self.extract_entities(text)
        return None