# ResumeSense: Multi-Agent based Smart Candidate Screening System 

## Overview
Welcome to the ResumeSense Repository, a cutting-edge project designed to streamline the recruitment process for HR professionals. This system automates the parsing, analysis, and ranking of candidate resumes against job descriptions, leveraging advanced AI techniques. It provides a user-friendly web interface for recruiters to upload files, view results, and interact with a chatbot for deeper insights. The project is currently under active development, with ongoing efforts to enhance each agent's performance to ensure robust and accurate results.

## Project Status
This project is still under progress, and I am currently working on enhancing each agent's performance to improve accuracy and functionality. The planned enhancements include:
- Training a custom spaCy model for Agent 1 (Keyword Extraction) to better extract resume-specific data.
- Fine-tuning the Transformers model for Agent 2 (Summarization) with resume-specific datasets for more relevant summaries.
- Upgrading Agent 3 (Similarity) to use Sentence-BERT for improved semantic matching.
- Enhancing Agent 4 (Chatbot Agent) with memory integration and tool usage for more context-aware interactions.
- Refining Agent 5 (Interview Question Generator) to generate more precise and relevant questions using advanced multi-step reasoning.

## Tech Stack
The project utilizes a diverse set of technologies to achieve its goals:
- **Programming Language**: Python
- **NLP Library**: spaCy for natural language processing tasks.
- **Language Model Library**: Hugging Face Transformers for summarization and advanced text processing.
- **AI Framework**: LangChain for building complex AI workflows, including RAG for the chatbot.
- **Vector Database**: FAISS for efficient document retrieval in the chatbot.
- **Web Frameworks**: Streamlit for initial fast deployment and Flask for the current web interface.
- **Front-End Technologies**: HTML, CSS, and JavaScript for creating an interactive and custom web UI.
- **File Parsing Libraries**: pdfplumber and python-docx for handling PDF and DOCX files.
- **Email Notifications**: mailjet for automated email notifications (Yet to incorporate with the frontend).

## Agents and Their Functions
The system comprises five specialized AI agents, each with a distinct role:

1. **Agent 1: Keyword Extraction (agent1_keyword_extraction.py)**  
   - **Function**: Uses spaCy to extract key entities such as skills, experience, education, and email from resumes, providing a structured overview for recruiters.
   - **Current Status**: Basic implementation with plans for custom training to improve accuracy on resume-specific data.

2. **Agent 2: Summarization (agent2_summarization.py)**  
   - **Function**: Employs a Transformers model (e.g., T5) to generate concise summaries of resumes, highlighting key details for quick review.
   - **Current Status**: Initial implementation with ongoing fine-tuning using resume-specific datasets for better relevance.

3. **Agent 3: Similarity Scoring (agent3_similarity.py)**  
   - **Function**: Calculates a similarity score (ATS score) between resumes and job descriptions to rank candidates, aiding in shortlisting.
   - **Current Status**: Uses TF-IDF with plans to upgrade to Sentence-BERT for enhanced semantic matching.

4. **Agent 4: Chatbot Agent (agent4_chatbot_agent.py)**  
   - **Function**: Utilizes Retrieval Augmented Generation (RAG) with LangChain and OpenAI to answer interactive queries about resumes and job descriptions, such as summarizing experience or explaining terms.
   - **Current Status**: Implements memory integration for context-aware interactions, with ongoing enhancements for tool usage.

5. **Agent 5: Interview Question Generator (agent5_InterviewQuestionGenerator.py)**  
   - **Function**: Generates tailored interview questions based on the resume and job description using multi-step reasoning with LangChain, assisting HR in candidate assessment.
   - **Current Status**: Initial implementation with plans to refine the reasoning process for more precise questions.

## Deployment
The project is deployed via Flask, providing a custom web interface where users can interact with the system after running the Flask application. Initially, Streamlit was used for fast deployment during prototyping, but the current implementation leverages Flask, HTML, CSS, and JavaScript for a more interactive and tailored user experience. The web interface allows users to upload resumes and job descriptions, view agent outputs, and engage with the chatbot.

## Getting Started
For detailed setup instructions, refer to the [Setup Instructions](setup.md).

## Contributors
- [Kathan Joshi](joshikathan03@gmail.com)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.