import streamlit as st
import os
from streamlit_chat import message
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

def ai_tutor():
    """
    AI Tutor: Handles a chat interface for learning AI/Data Science concepts
    """

    # --- LLM Setup ---
    groq_api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

    # --- Prompt Template ---
    prompt_template = """You are an experienced AI/Data Science/Data analytics tutor. 
Rules:
1) Answer only questions related to AI/Data Science and data analytics
2) Use real-world examples and fun explanations and in as tructured way
3) If question is unrelated, reply: "Sorry, I can only answer Data Science/AI related queries."
4) Maintain conversation context.

question: {query}
chat history: {chat_history}
"""
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm | StrOutputParser()

    # --- Function to generate response ---
    def generate_response(query, chat_history):
        return chain.invoke({
            "query": query,
            "chat_history": chat_history
        })

    # --- Streamlit UI ---
    st.title("📘 AI Learning Partner")
    st.info("Ask me anything about Data Science & AI!")

    # Initialize session state
    if "messages_ai" not in st.session_state:
        st.session_state.messages_ai = []
        st.session_state.chat_history_ai = []

    # Display chat messages
    for msg in st.session_state.messages_ai:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    query = st.chat_input("Ask a question about Data Science / AI")
    if query:
        # Store user message
        st.session_state.messages_ai.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # Generate response
        response = generate_response(query, st.session_state.chat_history_ai)
        st.session_state.messages_ai.append({"role": "assistant", "content": response})
        st.session_state.chat_history_ai.extend([HumanMessage(query.strip()), AIMessage(response)])

        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(response)
