from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain, SequentialChain
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = api_key

class InterviewQuestionAgent:
    def __init__(self):
        self._initialize_chains()

    def _initialize_chains(self):
        # Chain 1: Extract Relevant Info
        prompt1 = PromptTemplate(
            input_variables=["resume", "job_desc"],
            template="Given resume: {resume} and job desc: {job_desc}, list key relevant skills."
        )
        chain1 = LLMChain(
            llm=OpenAI(temperature=0),
            prompt=prompt1,
            output_key="relevant_info"  # Critical addition
        )

        # Chain 2: Identify Probe Areas
        prompt2 = PromptTemplate(
            input_variables=["relevant_info"],  # Now matches chain1's output
            template="Based on {relevant_info}, identify areas needing deeper probing."
        )
        chain2 = LLMChain(
            llm=OpenAI(temperature=0),
            prompt=prompt2,
            output_key="probe_areas"
        )

        # Chain 3: Generate Questions
        prompt3 = PromptTemplate(
            input_variables=["probe_areas"],  # Matches chain2's output
            template="Generate 5 interview questions for {probe_areas}."
        )
        chain3 = LLMChain(
            llm=OpenAI(temperature=0),
            prompt=prompt3,
            output_key="interview_questions"
        )

        self.overall_chain = SequentialChain(
            chains=[chain1, chain2, chain3],
            input_variables=["resume", "job_desc"],
            output_variables=["relevant_info", "probe_areas", "interview_questions"],
            verbose=True
        )

    def generate_questions(self, resume_text, job_desc_text):
        result = self.overall_chain({"resume": resume_text, "job_desc": job_desc_text})
        return result["interview_questions"]