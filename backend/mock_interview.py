import os
import streamlit as st
from streamlit_chat import message
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
import PyPDF2 as pdf

def mock_interview():
    # -----LLM Setup-----
    groq_api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

    # -----Prompt Template-----
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

    # -----Generate Response-----
    def generate_response(answer, chat_history, resume_text):
        return chain.invoke({
            "answer": answer,
            "chat_history": chat_history,
            "resume": resume_text
        })

    # -----Streamlit UI-----
    st.title("📄 Mock Interview Bot")
    st.info("Upload your resume to start the mock interview. Say **Hello** to begin!")

    # Upload resume
    resume_file = st.file_uploader("Upload resume (PDF)", type="pdf")
    if not resume_file:
        st.warning("Please upload your resume to continue.")
        st.stop()

    # Extract resume text
    reader = pdf.PdfReader(resume_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() or ""

    # Session state
    if "message_mi" not in st.session_state:
        st.session_state.message_mi = []
        st.session_state.chat_history_mi = []

    # Display previous chat messages
    for msg in st.session_state.message_mi:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input from user
    query = st.chat_input("Say Hello to start the interview! and if you want report , just type - Report")
    if query:
        # Store user message
        st.session_state.message_mi.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # Generate bot response
        response = generate_response(query, st.session_state.chat_history_mi, resume_text)
        st.session_state.message_mi.append({"role": "assistant", "content": response})
        st.session_state.chat_history_mi.extend([HumanMessage(query.strip()), AIMessage(response)])

        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(response)



if __name__ == "__main__":
     mock_interview()