import os
from dotenv import load_dotenv
from langchain_community.llms import OpenAI  # Updated import
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings  # New package
from langchain_community.vectorstores import FAISS  # Updated import
from langchain.chains import RetrievalQA  # Updated class

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
class ChatbotAgent:
    def __init__(self, resume_file_path, job_description_file_path):
        os.environ["OPENAI_API_KEY"] = api_key

        self.resume_text = self._load_file(resume_file_path)
        self.job_description_text = self._load_file(job_description_file_path)
        self.combined_text = self.resume_text + "\n\n" + self.job_description_text
        self._initialize_vector_store()
        self._initialize_qa_chain()
    def _load_file(self, file_path):
        from utils.file_parsing import parse_file
        return parse_file(file_path)

    def _split_text(self, text):
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return text_splitter.split_text(text)

    def _initialize_vector_store(self):
        texts = self._split_text(self.combined_text)
        embeddings = OpenAIEmbeddings()
        self.db = FAISS.from_texts(texts, embeddings)
        self._save_vector_store()

    def _save_vector_store(self):
        save_dir = os.path.join("models/summarization_model", os.path.basename(self.resume_file_path))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        index_path = os.path.join(save_dir, "index.faiss")
        self.db.index.faiss.write_index(index_path)

    def _load_vector_store(self, resume_file_path):
        save_dir = os.path.join("models/summarization_model", os.path.basename(resume_file_path))
        index_path = os.path.join(save_dir, "index.faiss")
        if os.path.exists(index_path):
            embeddings = OpenAIEmbeddings()
            index = faiss.read_index(index_path)
            self.db = FAISS(index=index, embeddings=embeddings)
        else:
            self._initialize_vector_store()

    def _initialize_qa_chain(self):
        llm = OpenAI(model="gpt-4o-mini")
        self.qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.db.as_retriever()
        )

    def answer_query(self, query):
        return self.qa.run(query)