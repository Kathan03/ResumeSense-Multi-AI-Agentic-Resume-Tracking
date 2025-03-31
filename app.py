from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import logging
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Then import other components
from agents.agent1_keyword_extraction import KeywordExtractionAgent
from agents.agent2_summarization import SummarizationAgent
from agents.agent3_similarity import SimilarityAgent
from agents.agent4_chatbot_agent import ChatbotAgent
from agents.agent5_InterviewQuestionGenerator import InterviewQuestionAgent
from utils.file_parsing import parse_file

app = Flask(__name__, static_folder='static', template_folder='templates')
# Use an absolute path for clarity – adjust as needed
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'data', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create upload directories if they don't exist
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resumes'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'job_descriptions'), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'resume' not in request.files or 'job_desc' not in request.files:
            logger.error("Upload error: Both files are required")
            return jsonify({"error": "Both files required"}), 400

        resume_file = request.files['resume']
        job_desc_file = request.files['job_desc']

        if resume_file.filename == '' or job_desc_file.filename == '':
            logger.error("Upload error: No file selected")
            return jsonify({"error": "No files selected"}), 400

        if not (allowed_file(resume_file.filename) and allowed_file(job_desc_file.filename)):
            logger.error("Upload error: Invalid file type")
            return jsonify({"error": "Invalid file type"}), 400

        # Secure filenames and build paths
        resume_filename = secure_filename(resume_file.filename)
        job_desc_filename = secure_filename(job_desc_file.filename)

        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resumes', resume_filename)
        job_desc_path = os.path.join(app.config['UPLOAD_FOLDER'], 'job_descriptions', job_desc_filename)

        # Save files
        resume_file.save(resume_path)
        job_desc_file.save(job_desc_path)

        logger.info(f"Files saved: {resume_path}, {job_desc_path}")

        return jsonify({
            "status": "success",
            "resume_filename": resume_filename,
            "job_desc_filename": job_desc_filename
        })

    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        return jsonify({"error": "File upload failed"}), 500

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        resume_filename = data.get('resume_filename')
        job_desc_filename = data.get('job_desc_filename')

        if not resume_filename or not job_desc_filename:
            return jsonify({"error": "Missing filenames"}), 400

        # Validate file paths
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resumes', resume_filename)
        job_desc_path = os.path.join(app.config['UPLOAD_FOLDER'], 'job_descriptions', job_desc_filename)

        if not os.path.exists(resume_path) or not os.path.exists(job_desc_path):
            return jsonify({"error": "Files not found"}), 404

        # Parse files with error handling
        try:
            resume_text = parse_file(resume_path)
            job_desc_text = parse_file(job_desc_path)
        except Exception as e:
            logger.error(f"Parsing failed: {str(e)}")
            return jsonify({"error": "File parsing failed"}), 500

        # Initialize agents with error handling
        try:
            agent1 = KeywordExtractionAgent()
            agent2 = SummarizationAgent()
            agent3 = SimilarityAgent()
            interview_agent = InterviewQuestionAgent()
        except Exception as e:
            logger.error(f"Agent initialization failed: {str(e)}")
            return jsonify({"error": "System initialization failed"}), 500

        # Process data
        try:
            results = {
                "keywords": agent1.process_resume(resume_path),
                "summary": agent2.process_resume(resume_path),
                "score": agent3.calculate_similarity(resume_text, job_desc_text),
                "questions": interview_agent.generate_questions(resume_text, job_desc_text)
            }
            return jsonify(results)
        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            return jsonify({"error": "Document processing failed"}), 500

    except Exception as e:
        logger.error(f"General processing error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/ask', methods=['POST'])
def handle_chat_query():
    try:
        data = request.get_json()
        resume_filename = data.get('resume_filename')
        job_desc_filename = data.get('job_desc_filename')
        query = data.get('query')

        if not all([resume_filename, job_desc_filename, query]):
            return jsonify({"error": "Missing parameters"}), 400

        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resumes', resume_filename)
        job_desc_path = os.path.join(app.config['UPLOAD_FOLDER'], 'job_descriptions', job_desc_filename)

        if not os.path.exists(resume_path) or not os.path.exists(job_desc_path):
            return jsonify({"error": "Files not found"}), 404

        try:
            chatbot = ChatbotAgent(resume_path, job_desc_path)
            response = chatbot.answer_query(query)
            return jsonify({"answer": response})
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return jsonify({"error": "Failed to process query"}), 500

    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/data/<path:filename>')
def uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)
