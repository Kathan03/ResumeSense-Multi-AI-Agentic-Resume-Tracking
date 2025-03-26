# test_chatbot.py
from agents.agent4_chatbot_agent import ChatbotAgent

def test_chatbot():
    try:
        bot = ChatbotAgent(
            "../data/resumes/KATHAN_JOSHI_RESUME.pdf",
            "../data/job_descriptions/ds.txt"
        )
        print(bot.answer_query("What technical skills are listed?"))
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_chatbot()