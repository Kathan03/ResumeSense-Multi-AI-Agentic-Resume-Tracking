import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


template = """You are an assistant that answers questions based on the provided context. If the context does not provide enough information to answer the question, you can use your own knowledge to answer it.

Question: {question}

Context: {context}

Please answer the question. If the context doesn't have enough information, use your general knowledge, but note if the answer is from general knowledge."""
prompt = PromptTemplate(input_variables=["question", "context"], template=template)

class ChatbotAgent:
    def __init__(self, resume_file_path, job_description_file_path):
        os.environ["OPENAI_API_KEY"] = api_key
        self.resume_file_path = resume_file_path
        self.job_description_filepath = job_description_file_path
        self.resume_text = self._load_file(resume_file_path)
        self.job_description_text = self._load_file(job_description_file_path)
        self.combined_text = self.resume_text + "\n\n" + self.job_description_text
        self._initialize_vector_store()
        self._initialize_qa_chain()

    def _load_file(self, file_path):
        from utils.file_parsing import parse_file
        text = parse_file(file_path)
        if text:
            # print(text)
            return text
        return None

    def _split_text(self, text):
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return text_splitter.split_text(text)

    def _initialize_vector_store(self):
        texts = self._split_text(self.combined_text)
        embeddings = OpenAIEmbeddings()
        self.db = FAISS.from_texts(texts, embeddings)
        self._save_vector_store()

    def _save_vector_store(self):
        try:
            base_name = os.path.basename(self.resume_file_path).split('.')[0]  # Get filename without extension
            save_dir = os.path.join(BASE_DIR, "models", "summarization_model", base_name)

            # Create directory if not exists
            os.makedirs(save_dir, exist_ok=True)

            index_path = os.path.join(save_dir, "index.faiss")
            self.db.save_local(folder_path=save_dir)  # Use FAISS's built-in save method
        except Exception as e:
            print(f"Vector Store Save Error: {str(e)}")
            raise

    def _load_vector_store(self, resume_file_path):
        base_name = os.path.basename(resume_file_path).split('.')[0]
        save_dir = os.path.join(BASE_DIR, "models", "summarization_model", base_name)
        if os.path.exists(save_dir):
            embeddings = OpenAIEmbeddings()
            self.db = FAISS.load_local(save_dir, embeddings)
        else:
            self._initialize_vector_store()

    def _initialize_qa_chain(self):
        # Change from deprecated OpenAI to ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini")  # or "gpt-3.5-turbo"

        # Update retrieval chain
        self.qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.db.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

    def answer_query(self, query):
        response = self.qa.invoke({"query": query})
        return response["result"]