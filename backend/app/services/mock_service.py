import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

prompt_template = """You are a technical recruiter interviewing for data science/AI.
Analyze resume and ask scenario-based practical questions.
Validate answers using STAR methodology (internal).
Do not repeat questions.
Provide report when requested.

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
