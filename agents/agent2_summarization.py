from transformers import T5Tokenizer, T5ForConditionalGeneration

class SummarizationAgent:
    def __init__(self, model_name="t5-small"):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)

    def summarize_text(self, text, max_length=100):
        """Generate a summary of the given text."""
        input_text = "summarize: " + text
        inputs = self.tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = self.model.generate(inputs["input_ids"], max_length=max_length, num_beams=4, early_stopping=True)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    def process_resume(self, file_path):
        """Process a resume file and return its summary."""
        from utils.file_parsing import parse_file
        text = parse_file(file_path)
        if text:
            return self.summarize_text(text)
        return None