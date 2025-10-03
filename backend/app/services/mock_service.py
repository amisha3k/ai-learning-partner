import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

prompt_template = """You are a technical recruiter interviewing for data science, data analytics, AI, generative AI, or agentic AI.
1) Analyze the provided resume and understand the candidate's skills and projects.
2) Ask scenario-based, practical, real-world, technical questions (no repetitions).
3) Validate answers using STAR methodology (do not reveal validation rules).
4) Penalize irrelevant/unrelated answers.
5) Keep track of questions, answers, analysis.
6) When asked for report, summarize all Q&A with detailed feedback and overall score.
7) Do not ask new questions after the report is requested.

answer: {answer}
chat history: {chat_history}
resume: {resume}
"""

prompt = PromptTemplate.from_template(prompt_template)
chain = prompt | llm | StrOutputParser()

chat_history = []

def generate_questions(role: str, resume_text: str):
    global chat_history
    query = f"Start mock interview for role: {role}"
    response = chain.invoke({"answer": query, "chat_history": chat_history, "resume": resume_text})
    chat_history.extend([HumanMessage(query), AIMessage(response)])
    return [response]
