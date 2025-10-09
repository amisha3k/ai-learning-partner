# import os
# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

# groq_api_key = os.getenv("GROQ_API_KEY")
# llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

# prompt_template = """You are a technical recruiter interviewing for data science/AI.
# Analyze resume and ask scenario-based practical questions.
# Validate answers using STAR methodology (internal).
# Do not repeat questions.
# Provide report when requested.

# answer: {answer}
# chat history: {chat_history}
# resume: {resume}
# """

# prompt = PromptTemplate.from_template(prompt_template)
# chain = prompt | llm | StrOutputParser()

# chat_history = []

# def generate_questions(role: str, resume_text: str):
#     global chat_history
#     query = f"Start mock interview for role: {role}"
#     response = chain.invoke({"answer": query, "chat_history": chat_history, "resume": resume_text})
#     chat_history.extend([HumanMessage(query), AIMessage(response)])
#     return [response]

import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

# In-memory session store
sessions = {}

# Initialize LLM
# llm = ChatGroq(model="gpt-4o-mini")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))


def start_interview(role: str):
    """Start a new mock interview session."""
    session_id = str(len(sessions) + 1)
    sessions[session_id] = {"role": role, "history": []}

    prompt_template = f"""
    You are an AI interviewer for the role of {role}.
    Start the interview by greeting the candidate and asking the first question.
    Ask only one question at a time.
    """
    question = llm.invoke(prompt_template)
    sessions[session_id]["history"].append({"interviewer": question.content})

    return session_id, question.content


def process_message(session_id: str, message: str):
    """Handle user messages during the interview."""
    if session_id not in sessions:
        return "Invalid session. Please start again.", True

    msg = message.strip().lower()

    if msg == "stop":
        return "Interview stopped. Goodbye!", True

    if msg == "report":
        return generate_report(session_id), True

    if msg == "start":
        return next_question(session_id), False

    # Otherwise, treat as candidate’s answer
    sessions[session_id]["history"][-1]["candidate"] = message
    feedback = give_feedback(session_id, message)
    sessions[session_id]["history"].append({"interviewer": feedback})
    return feedback, False


def give_feedback(session_id: str, answer: str):
    """Generate feedback and next question."""
    role = sessions[session_id]["role"]
    prompt = f"""
    You are an AI interviewer for a {role} position.
    The candidate answered: "{answer}"

    Step 1: Give short feedback (2 sentences).
    Step 2: Ask the next technical question in the interview.
    """
    feedback = llm.invoke(prompt)
    return feedback.content


def next_question(session_id: str):
    """Ask next interview question manually using 'start'."""
    role = sessions[session_id]["role"]
    prompt = f"""
    Continue the mock interview for {role}.
    Ask the next relevant technical question. Only one question.
    """
    question = llm.invoke(prompt)
    sessions[session_id]["history"].append({"interviewer": question.content})
    return question.content


def generate_report(session_id: str):
    """Generate a summary report from the Q&A history."""
    role = sessions[session_id]["role"]
    history = sessions[session_id]["history"]
    transcript = "\n".join(
        [f"Q: {h.get('interviewer')} A: {h.get('candidate', 'Not answered')}" for h in history]
    )

    prompt = f"""
    You are an  interviewer for the role of {role}.
    Based on this interview transcript, write a performance report
    summarizing the candidate's strengths, weaknesses, and recommendations and give points out of hundered.

    Transcript:
    {transcript}
    """
    report = llm.invoke(prompt)
    return report.content
