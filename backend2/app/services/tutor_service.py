import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

# Initialize LLM
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

# Prompt template
prompt_template = """You are an experienced AI/Data Science/Data analytics tutor. 
Rules:
1) Answer only questions related to AI/Data Science and data analytics
2) Use real-world examples and fun explanations
3) If question is unrelated, reply: "Sorry, I can only answer Data Science/AI queries."
4) Maintain conversation context.

question: {query}
chat history: {chat_history}
"""

prompt = PromptTemplate.from_template(prompt_template)
chain = prompt | llm | StrOutputParser()

# Simple function for backend
chat_history = []

def get_tutor_answer(query: str) -> str:
    global chat_history
    response = chain.invoke({"query": query, "chat_history": chat_history})
    chat_history.extend([HumanMessage(query), AIMessage(response)])
    return response
